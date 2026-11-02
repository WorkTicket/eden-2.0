"""SQLite-backed persistence for the continuous simulation.

Design (see plan Section 5):
- Single authoritative SQLite database per run.
- Checkpoints are versioned and archived (never overwrite the sole checkpoint).
- Append-only event table alongside checkpoints; JSONL remains an export format.
- Atomic writes; tests cover corrupt-checkpoint recovery and schema mismatch.

Schema version 1 stores: world state, agents (persona ref + cognitive state),
logical clock, pending actions, random-generator state, and the event log sequence
number. Restoration validates references and resumes unfinished actions.
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    tick INTEGER NOT NULL,
    agent TEXT NOT NULL,
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL,
    hunger REAL NOT NULL,
    payload TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seq INTEGER NOT NULL,
    tick INTEGER NOT NULL,
    payload TEXT NOT NULL,
    archived INTEGER NOT NULL DEFAULT 0,
    created_at REAL NOT NULL
);
"""


class CheckpointStore:
    """Transaction-backed checkpoint store for one simulation run."""

    def __init__(self, run_dir: Path | str) -> None:
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.run_dir / "state.db"
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.executescript(_SCHEMA)
        self._conn.commit()
        self._ensure_meta()

    def _ensure_meta(self) -> None:
        cur = self._conn.execute("SELECT value FROM meta WHERE key='schema_version'")
        row = cur.fetchone()
        if row is None:
            self._conn.execute(
                "INSERT INTO meta(key, value) VALUES ('schema_version', ?)",
                (str(SCHEMA_VERSION),),
            )
            self._conn.commit()
        elif int(row[0]) != SCHEMA_VERSION:
            raise ValueError(
                f"schema mismatch: store is v{row[0]}, code expects v{SCHEMA_VERSION}"
            )

    def close(self) -> None:
        self._conn.close()

    def append_event(self, tick: int, agent: str, action: str, result: str,
                     pos: tuple[int, int], hunger: float, payload: dict[str, Any]) -> int:
        cur = self._conn.execute(
            "INSERT INTO events(tick, agent, action, result, pos_x, pos_y, hunger, payload)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tick, agent, action, result, int(pos[0]), int(pos[1]), float(hunger),
             json.dumps(payload)),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def last_seq(self) -> int:
        cur = self._conn.execute("SELECT COALESCE(MAX(seq), 0) FROM events")
        return int(cur.fetchone()[0])

    def save_checkpoint(self, tick: int, seq: int, payload: dict[str, Any],
                        archive_previous: bool = True) -> int:
        """Atomically save a checkpoint, archiving the previous live one."""
        if archive_previous:
            self._conn.execute(
                "UPDATE checkpoints SET archived=1 WHERE archived=0"
            )
        cur = self._conn.execute(
            "INSERT INTO checkpoints(seq, tick, payload, archived, created_at)"
            " VALUES (?, ?, ?, 0, ?)",
            (seq, tick, json.dumps(payload), time.time()),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def load_latest_checkpoint(self) -> dict[str, Any] | None:
        cur = self._conn.execute(
            "SELECT payload FROM checkpoints WHERE archived=0 ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def load_events_after(self, seq: int) -> list[dict[str, Any]]:
        cur = self._conn.execute(
            "SELECT tick, agent, action, result, pos_x, pos_y, hunger, payload"
            " FROM events WHERE seq > ? ORDER BY seq",
            (seq,),
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]

    def export_jsonl(self, path: Path | str) -> None:
        """Export the append-only event log as JSONL (for the baked viewer)."""
        cur = self._conn.execute(
            "SELECT tick, agent, action, result, pos_x, pos_y, hunger, payload"
            " FROM events ORDER BY seq"
        )
        with open(path, "w", encoding="utf-8") as f:
            for row in cur.fetchall():
                f.write(json.dumps({
                    "tick": row[0], "agent": row[1], "action": row[2],
                    "result": row[3], "pos": [row[4], row[5]],
                    "hunger": round(row[6], 3), **json.loads(row[7]),
                }) + "\n")
