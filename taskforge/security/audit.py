# -*- coding: utf-8 -*-
"""Deterministic code audit: flag risky patterns in source code.

The mock auditor flags a risky pattern when the model skill is high and misses it
otherwise (boost = (skill - 0.5) * 2). Ground truth patterns are a fixed set.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

RISKY_PATTERNS = ["eval(", "exec(", "subprocess.", "shell=True", "pickle.loads", "os.system"]


@dataclass
class CodeAuditor:
    skill: float = 0.5

    def audit(self, code: str) -> Dict:
        from ..utils.stable import stable_bool
        flags = []
        for pat in RISKY_PATTERNS:
            boost = (self.skill - 0.5) * 2.0
            hit = stable_bool("audit:" + pat + ":" + code[:40], p=0.5 + 0.5 * boost)
            if pat in code and hit:
                flags.append(pat)
        return {"flags": flags, "risk_level": "high" if flags else "low"}


def audit_code(code: str, skill: float = 1.0) -> Dict:
    return CodeAuditor(skill=skill).audit(code)
