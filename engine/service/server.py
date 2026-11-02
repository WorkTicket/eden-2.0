"""Lightweight HTTP operator interface for the live runtime.

Endpoints (read-only unless noted):
  GET  /state      -> current runtime snapshot (read-only view for the viewer)
  GET  /events?n=50-> recent committed events
  GET  /control    -> {running, tick, day}
  POST /control    -> {"action": "play"|"pause"|"stop"}
  GET  /export     -> JSONL of the full event log (for the baked viewer)

Runs in a background thread so the simulation keeps ticking while an operator
or viewer polls state. Researcher diagnostics (structured goals, evidence,
outcome summaries) are exposed here only, never inhabitant perception.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Optional

from engine.service.runtime import Runtime


class _Handler(BaseHTTPRequestHandler):
    runtime: Optional[Runtime] = None  # set by the server factory

    def _send(self, code: int, payload: dict | str, content_type: str = "application/json") -> None:
        if isinstance(payload, dict):
            body = json.dumps(payload).encode("utf-8")
        else:
            body = payload.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        rt: Runtime = self.server.runtime  # type: ignore[attr-defined]
        if path == "/state":
            self._send(200, rt.current_state())
        elif path == "/events":
            n = 50
            try:
                n = int(self.path.split("n=")[1].split("&")[0])
            except Exception:
                pass
            self._send(200, rt.recent_events(n))
        elif path == "/control":
            self._send(200, {"running": rt.playing(), "tick": rt.clock.tick, "day": rt.clock.day})
        elif path == "/export":
            # Stream the JSONL export to a temp file then return it as text
            out = Path(self.server.run_dir) / "events_export.jsonl"
            rt.store.export_jsonl(out)
            self._send(200, out.read_text(encoding="utf-8"), "application/x-jsonlines")
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        path = self.path.split("?", 1)[0]
        rt: Runtime = self.server.runtime  # type: ignore[attr-defined]
        if path == "/control":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                action = json.loads(body.decode("utf-8")).get("action", "")
            except Exception:
                action = ""
            if action == "play":
                if not rt.playing():
                    threading.Thread(target=rt.play, daemon=True).start()
                self._send(200, {"ok": True, "action": "play", "running": rt.playing()})
            elif action == "pause":
                rt.pause()
                self._send(200, {"ok": True, "action": "pause"})
            elif action == "stop":
                rt.stop()
                self._send(200, {"ok": True, "action": "stop"})
            else:
                self._send(400, {"error": "unknown action"})
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, fmt, *args):  # silence default stderr logging
        return


class LiveServer:
    """Background HTTP server exposing a read-only view of the Runtime."""

    def __init__(self, rt: Runtime, host: str = "127.0.0.1", port: int = 8765) -> None:
        self.rt = rt
        self.run_dir = rt.run_dir
        self._server = ThreadingHTTPServer((host, port), _Handler)
        self._server.runtime = rt  # type: ignore[attr-defined]
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    @property
    def url(self) -> str:
        return f"http://{self._server.server_address[0]}:{self._server.server_address[1]}"
