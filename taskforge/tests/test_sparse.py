# -*- coding: utf-8 -*-
import unittest

from taskforge.sparse.attention import full_attention, sparse_attention
from taskforge.sparse.router import BlockRouter
from taskforge.utils.stable import stable_vector


class TestSparse(unittest.TestCase):
    def test_full_attention_normalizes(self):
        q = stable_vector("q", 32)
        keys = [stable_vector("k%d" % i, 32) for i in range(16)]
        w = full_attention(q, keys)
        self.assertAlmostEqual(sum(w), 1.0, places=5)

    def test_router_selects_gold_at_high_skill(self):
        r = BlockRouter(top_k=2)
        sel = r.select("seq-0", 4, [0, 1], 1.0)
        self.assertEqual(set(sel), {0, 1})

    def test_sparse_attention_smaller(self):
        q = stable_vector("q", 32)
        keys = [stable_vector("k%d" % i, 32) for i in range(64)]
        out = sparse_attention(q, keys, block_size=16, top_k=2, gold_blocks=[0, 1],
                               skill=1.0, seq_key="s")
        self.assertEqual(len(out), 32)  # 2 blocks * 16


if __name__ == "__main__":
    unittest.main()
