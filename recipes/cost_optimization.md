# 配方：成本优化

```python
from taskforge.metrics.cost import estimate_cost
print("CNY:", estimate_cost(in_tokens=10000, out_tokens=2000))
```

要点：思考预算按步衰减 → 输入 token 下降 → 成本随 skill 提升而下降。
