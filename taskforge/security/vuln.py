# -*- coding: utf-8 -*-
"""Deterministic vulnerability scanner over a synthetic package surface."""
from __future__ import annotations

from typing import Dict, List

from ..utils.stable import stable_ints


class VulnScanner:
    def __init__(self, skill: float = 0.5):
        self.skill = skill

    def scan(self, surface_id: str, n_pkgs: int = 20) -> Dict:
        boost = (self.skill - 0.5) * 2.0
        n_vuln = stable_ints("vuln:n:" + surface_id, 1, 1, 6)[0]
        # ground-truth vulnerable package indices
        vuln_idx = sorted(set(stable_ints("vuln:idx:" + surface_id, n_vuln, 0, n_pkgs - 1)))
        found = [i for i in vuln_idx if (self.skill > 0.5 and i in vuln_idx)]
        # recall: fraction of true vulns found
        recall = (len(found) / len(vuln_idx)) if vuln_idx else 1.0
        return {"surface": surface_id, "true_vulns": len(vuln_idx), "found": len(found),
                "recall": recall}


def scan_vulns(surface_id: str, skill: float = 1.0) -> Dict:
    return VulnScanner(skill=skill).scan(surface_id)
