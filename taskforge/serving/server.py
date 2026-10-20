# -*- coding: utf-8 -*-
"""Zero-dependency HTTP server (stdlib http.server).

Endpoints:
  GET  /health           -> {"status": "ok"}
  GET  /v1/models        -> {"models": [5 backends]}
  POST /v1/plan          -> {"goal_id": ..., "plan": [...]}
  POST /v1/run           -> full workflow result
  POST /v1/ground        -> GUI grounding result
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional

from ..config import Config
from ..engine import TaskforgeEngine
from ..model.backends import list_backends


def _load(body: bytes) -> dict:
    if not body:
        return {}
    try:
        return json.loads(body.decode("utf-8"))
    except Exception:
        return {}


class _Handler(BaseHTTPRequestHandler):
    engine: Optional[TaskforgeEngine] = None

    def _send(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        if self.path == "/v1/models":
            return self._send(200, {"models": list_backends()})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        body = _load(self.rfile.read(int(self.headers.get("Content-Length", 0) or 0)))
        if self.path == "/v1/plan":
            goal = body.get("goal_id", "goal-0")
            plan = self.engine.backend.plan(goal)
            return self._send(200, {"goal_id": goal, "plan": plan})
        if self.path == "/v1/run":
            goal = body.get("goal_id", "goal-0")
            res = self.engine.run(goal)
            return self._send(200, res.to_dict())
        if self.path == "/v1/ground":
            sid = body.get("screen_id", "scr-0")
            iid = body.get("intent_id", "intent-0")
            from ..oracle import screen_elements
            elements = screen_elements(sid, self.engine.cfg.gui.n_elements)
            element_id, action = self.engine.backend.ground(sid, iid, elements)
            return self._send(200, {"screen_id": sid, "intent_id": iid,
                                    "element": element_id, "action": action})
        return self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def run_server(cfg=None, host="127.0.0.1", port=8787):
    cfg = cfg or Config()
    engine = TaskforgeEngine(cfg)
    handler = type("Handler", (_Handler,), {"engine": engine})
    server = HTTPServer((host, port), handler)
    print("[serve] taskforge listening on http://%s:%d" % (host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
