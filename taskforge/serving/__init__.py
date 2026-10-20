# -*- coding: utf-8 -*-
"""HTTP serving + CLI for taskforge (zero-dependency, stdlib http.server)."""


def serve(cfg=None, host="127.0.0.1", port=8787):
    from .server import run_server
    run_server(cfg, host, port)


def main(argv=None):
    from .cli import main as _main
    return _main(argv)


__all__ = ["serve", "main"]
