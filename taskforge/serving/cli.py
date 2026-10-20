# -*- coding: utf-8 -*-
"""Command-line interface: doctor / bench / train / run / serve."""
from __future__ import annotations

import argparse
import json
import sys

from ..config import Config, load_config
from ..engine import TaskforgeEngine
from ..model.backends import get_backend, list_backends
from ..train import train
from ..bench.registry import run_all as bench_run_all


def _doctor(cfg):
    print("[doctor] backends: %s" % ", ".join(list_backends()))
    backend = get_backend(cfg.model.backend, cfg)
    # plan smoke
    plan = backend.plan("goal-0")
    print("[doctor] plan(goal-0) -> %s" % plan)
    # tool smoke
    tool = backend.choose_tool("search")
    print("[doctor] choose_tool(search) -> %s" % tool)
    # ground smoke
    from ..oracle import screen_elements
    elements = screen_elements("scr-0", cfg.gui.n_elements)
    el, act = backend.ground("scr-0", "intent-0", elements)
    print("[doctor] ground(scr-0) -> (%s, %s)" % (el, act))
    # sparse smoke
    from ..sparse.attention import sparse_attention
    from ..utils.stable import stable_vector
    q = stable_vector("q", cfg.sparse.dim)
    keys = [stable_vector("k%d" % i, cfg.sparse.dim) for i in range(cfg.sparse.seq_len)]
    out = sparse_attention(q, keys, cfg.sparse.block_size, cfg.sparse.top_k,
                           [0, 1], 0.5, "seq-0")
    print("[doctor] sparse_attention -> %d weights" % len(out))
    # engine smoke
    eng = TaskforgeEngine(cfg)
    res = eng.run("goal-0")
    print("[doctor] engine.run(goal-0) -> success=%s steps=%d" % (res.success, len(res.steps)))
    print("[doctor] declared scale: %.0fB total / %.0fB active / %d ctx / %d tps"
          % (cfg.total_params_b, cfg.active_params_b, cfg.context_window, cfg.tokens_per_second))
    return True


def _bench(cfg):
    backend = get_backend(cfg.model.backend, cfg)
    print("[bench] skill before train: %.4f" % backend.skill)
    train(backend)
    print("[bench] skill after train: %.4f" % backend.skill)
    results = bench_run_all(cfg, backend)
    for name, r in results.items():
        print("[bench] %-12s %s" % (name, json.dumps(r, ensure_ascii=False)))
    return results


def _serve(cfg, host, port):
    from .server import run_server
    run_server(cfg, host, port)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="taskforge", description="long-horizon agent workflow engine")
    parser.add_argument("--config", default=None, help="path to config.yaml")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("doctor", help="run a full smoke check")
    sub.add_parser("bench", help="train + run all benchmarks")
    sub.add_parser("train", help="train the mock backend")
    p_run = sub.add_parser("run", help="run a workflow for a goal")
    p_run.add_argument("--goal", default="goal-0")
    p_serve = sub.add_parser("serve", help="start the HTTP server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8787)

    args = parser.parse_args(argv)
    cfg = load_config(args.config)

    if args.command in (None, "doctor"):
        _doctor(cfg)
    elif args.command == "bench":
        _bench(cfg)
    elif args.command == "train":
        backend = get_backend(cfg.model.backend, cfg)
        hist = train(backend)
        print("[train] skill %.4f -> %.4f" % (hist[0][1], hist[-1][1]))
    elif args.command == "run":
        eng = TaskforgeEngine(cfg)
        res = eng.run(args.goal)
        print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
    elif args.command == "serve":
        _serve(cfg, args.host, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
