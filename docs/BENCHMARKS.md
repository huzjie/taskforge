# 基准说明

五个基准共用 `bench/registry.py` 的 `run_all(cfg, backend)`：

1. **planning** — 多步规划成功率（子目标序列是否按序覆盖 oracle 真值）
2. **tools** — 工具链准确率（每个子目标是否选对工具）
3. **gui** — GUI 动作接地准确率（是否命中目标元素 + 合法动作）
4. **sparse** — 稀疏注意力加速比（结构常数）+ 黄金块召回率（随 skill）
5. **longhorizon** — 长程完成率（无恢复 vs 有卡点恢复）

跑法：`python -m taskforge bench`。
