import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from taskforge.security.audit import audit_code
from taskforge.security.vuln import scan_vulns
from taskforge.security.sandbox import run_in_sandbox

print("audit :", audit_code("x = eval(user_input)", skill=1.0))
print("vuln  :", scan_vulns("surface-0", skill=1.0))
print("sandbox:", run_in_sandbox("eval('1+1')"))
