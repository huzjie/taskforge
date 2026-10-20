# 组件说明

| 模块 | 职责 | 关键实现 |
| --- | --- | --- |
| `planner` | 目标 → 子目标 DAG + ReAct | `decompose` / `react_loop` / `ThinkingBudget` |
| `tools` | 工具链编排 | schema 绑定 + 校验 + 重试/回滚 |
| `gui` | 电脑操作动作接地 | 屏幕元素树 + 目标元素 + 跨应用状态机 |
| `memory` | 长程工作记忆 | 进度追踪 + 卡点检测 + 恢复 |
| `sparse` | 稀疏注意力加速 | index 分支选块 + sparse 分支 top-k softmax |
| `model` | 5 后端统一接口 | mock(可训练)/openai/vllm/transformers/anthropic |
| `bench` | 5 基准 | 规划/工具链/GUI/稀疏/长程 |
