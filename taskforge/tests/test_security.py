# -*- coding: utf-8 -*-
import unittest

from taskforge.security.audit import audit_code
from taskforge.security.vuln import scan_vulns
from taskforge.security.sandbox import run_in_sandbox


class TestSecurity(unittest.TestCase):
    def test_audit_flags_eval(self):
        r = audit_code("x = eval(user_input)", skill=1.0)
        self.assertIn("eval(", r["flags"])

    def test_sandbox_blocks_eval(self):
        r = run_in_sandbox("eval('1+1')")
        self.assertFalse(r["safe"])

    def test_vuln_recall_perfect(self):
        r = scan_vulns("surface-0", skill=1.0)
        self.assertAlmostEqual(r["recall"], 1.0, places=3)


if __name__ == "__main__":
    unittest.main()
