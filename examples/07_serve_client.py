import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
"""Hit a running `python -m taskforge serve` instance over HTTP (stdlib only)."""
import json
import urllib.request

BASE = "http://127.0.0.1:8787"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


def post(path, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE + path, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as r:
        return json.loads(r.read().decode("utf-8"))


if __name__ == "__main__":
    print("health :", get("/health"))
    print("models :", get("/v1/models"))
    print("plan   :", post("/v1/plan", {"goal_id": "goal-0"}))
