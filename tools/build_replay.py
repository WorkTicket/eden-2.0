"""Bake a run into a self-contained viewer: python tools/build_replay.py data/runs/<run_id>

Writes engine/viz/viewer.fragment.html (for embedding / Artifact publishing) and
engine/viz/viewer.html (standalone: open directly in a browser).
"""
import json
import sys
from pathlib import Path

import yaml

from engine.persistence import CheckpointStore

ROOT = Path(__file__).resolve().parents[1]
VIZ = ROOT / "engine" / "viz"


def _load_events(run_dir: Path) -> list[dict]:
    events_path = run_dir / "events.jsonl"
    if events_path.exists():
        with open(events_path, encoding="utf-8") as f:
            return [json.loads(line) for line in f]
    # Continuous runs write to SQLite; export the append-only event log to JSONL.
    db = run_dir / "state.db"
    if db.exists():
        store = CheckpointStore(run_dir)
        try:
            store.export_jsonl(events_path)
        finally:
            store.close()
        with open(events_path, encoding="utf-8") as f:
            return [json.loads(line) for line in f]
    raise FileNotFoundError(f"no events.jsonl or state.db in {run_dir}")


def build(run_dir: Path) -> dict:
    events = _load_events(run_dir)
    ids = sorted({e["agent"] for e in events})
    agents = []
    for i in ids:
        snap = run_dir / "snapshots" / f"{i}.json"
        name = json.loads(snap.read_text())["persona"] if snap.exists() else i
        agents.append({"id": i, "name": name})
    idx = {a["id"]: n for n, a in enumerate(agents)}
    return {
        "map": yaml.safe_load((ROOT / "world" / "maps" / "eden.yaml").read_text(encoding="utf-8")),
        "laws": yaml.safe_load((ROOT / "world" / "laws" / "physics.yaml").read_text(encoding="utf-8")),
        "agents": agents,
        "ticks": max(e["tick"] for e in events) + 1,
        "events": [[e["tick"], idx[e["agent"]], e["action"], e["result"], e["pos"][0], e["pos"][1], e["hunger"]]
                   for e in events],
    }


def main(run_dir: str) -> None:
    data = json.dumps(build(Path(run_dir)), separators=(",", ":")).replace("</", "<\\/")
    tmpl = (VIZ / "viewer_template.html").read_text(encoding="utf-8")
    assert "/*REPLAY_DATA*/ null" in tmpl, "template placeholder missing"
    fragment = tmpl.replace("/*REPLAY_DATA*/ null", data)
    (VIZ / "viewer.fragment.html").write_text(fragment, encoding="utf-8")
    (VIZ / "viewer.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<style>html,body{margin:0}</style></head><body>" + fragment + "</body></html>",
        encoding="utf-8",
    )
    print(VIZ / "viewer.html")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tools/build_replay.py data/runs/<run_id>")
    main(sys.argv[1])
