# 配方：稀疏注意力提速

```python
from taskforge.sparse.attention import sparse_attention
out = sparse_attention(q, keys, block_size=16, top_k=4, gold_blocks=[0, 1], skill=1.0)
```

要点：加速比 ≈ n_blocks / top_k；top_k 越小越快，但要保证黄金块召回率。
