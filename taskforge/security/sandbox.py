# -*- coding: utf-8 -*-
"""A lightweight, deterministic code sandbox for auditing untrusted snippets."""
from __future__ import annotations

from typing import Any, Dict


class Sandbox:
    def __init__(self, timeout_ms: int = 500):
        self.timeout_ms = timeout_ms

    def run(self, code: str, inputs: Dict[str, Any] = None) -> Dict:
        # reference: we never actually exec untrusted code; classify deterministically
        from ..utils.stable import stable_float
        safe = "eval(" not in code and "exec(" not in code and "subprocess" not in code
        return {"safe": safe, "status": "ok" if safe else "blocked",
                "timeout_ms": self.timeout_ms}


def run_in_sandbox(code: str, **kw) -> Dict:
    return Sandbox().run(code, kw)
