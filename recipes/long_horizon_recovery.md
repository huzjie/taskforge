# 配方：长程任务卡点恢复

```python
from taskforge.memory.working import WorkingMemory
from taskforge.config import Config

mem = WorkingMemory(Config().memory)
for step in steps:
    if ok:
        mem.mark_progress(step)
    elif mem.record_stall(step):   # 连续失败达到阈值 → 触发恢复
        retry(step)
```

要点：卡点检测用「连续失败计数」而非单次失败，避免偶发抖动触发无谓重试。
