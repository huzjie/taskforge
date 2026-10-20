# -*- coding: utf-8 -*-
"""Sparse attention: index branch selects blocks, sparse branch does top-k softmax."""
from .attention import sparse_attention, full_attention
from .router import BlockRouter, block_scores

__all__ = ["sparse_attention", "full_attention", "BlockRouter", "block_scores"]
