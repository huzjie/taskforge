import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taskforge.config import Config
from taskforge.sparse.attention import full_attention, sparse_attention
from taskforge.utils.stable import stable_vector

cfg = Config()
dim = cfg.sparse.dim
seq_len = cfg.sparse.seq_len
block_size = cfg.sparse.block_size
top_k = cfg.sparse.top_k

q = stable_vector("q", dim)
keys = [stable_vector("k%d" % i, dim) for i in range(seq_len)]

full = full_attention(q, keys)
sparse = sparse_attention(q, keys, block_size, top_k, [0, 1], 1.0, "demo")
n_blocks = (seq_len + block_size - 1) // block_size

print("full attention weights: %d" % len(full))
print("sparse attention weights: %d" % len(sparse))
print("speedup ~ n_blocks/top_k = %.1fx" % (n_blocks / top_k))
