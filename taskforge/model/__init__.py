# -*- coding: utf-8 -*-
"""Model backends: a uniform interface over mock / openai / vllm / transformers /
anthropic. The mock backend is deterministic and trainable (skill 0.5 -> 1.0)."""
from .backends import get_backend, list_backends, register_backend

__all__ = ["get_backend", "list_backends", "register_backend"]
