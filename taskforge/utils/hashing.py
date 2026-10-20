# -*- coding: utf-8 -*-
"""Content addressing helpers."""
from __future__ import annotations

import hashlib


def md5_hex(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
