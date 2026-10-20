# 调参指南

| 参数 | 位置 | 建议 |
| --- | --- | --- |
| `sparse.top_k` | config | 越小越快，但要保证黄金块召回率 |
| `sparse.block_size` | config | 块越大 n_blocks 越少，加速比下降 |
| `memory.stall_threshold` | config | 太低误触发，太高响应慢 |
| `planner.thinking_budget` | config | 预算越大思考越充分，成本越高 |
| `model.temperature` | config | mock 保持 0.0 确定性 |

原则：先 `doctor` 验证基线，再 `bench` 看 skill 曲线，最后调 top_k 换速度。
