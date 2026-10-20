# taskforge 架构说明

## 一句话

taskforge 是「复杂长程智能体工作流编排引擎」的零依赖参考实现，把 MiniMax M3.1 Flash
（太空兔）在复杂 Agent 任务上的能力拆成五个可复用的工程件：**多步规划、连续工具调用、
电脑操作（GUI）动作接地、长程工作记忆、稀疏注意力推理加速**。

## 分层

```
goal (自然语言目标)
   │
   ▼
planner ── decompose → 有序子目标序列 / DAG
   │
   ▼
tools ── orchestrate → 每个子目标绑定工具 + 参数 + 校验 + 重试/回滚
   │
   ▼
gui ── ground → (screen, intent) → (element, action)   [仅 GUI 型任务]
   │
   ▼
memory ── track → 进度 / 卡点检测 / 恢复
   │
   ▼
sparse ── accelerate → index 分支选块 + sparse 分支 top-k softmax
```

## 核心设计决策

1. **单一真值 oracle**：`oracle.py` 是 mock 后端与所有基准共享的确定性真值来源，
   skill=1.0 必然满分、skill=0.5 是随机基线，所有数字可复现。
2. **单调训练信号**：`boost = (skill - 0.5) * 2`，skill=0.5 时 boost 恰为 0，
   skill=1.0 恒正确，绝不使用「对 +1 / 错 -1」的随机游走。
3. **零依赖**：内置 `utils/yamlish.py` 极简 YAML 解析、`utils/stable.py` md5 种子确定性随机，
   不依赖 numpy/pyyaml/requests。
4. **声明规模与实例化解耦**：560B 总参 / 25B 激活 / 1M 上下文 / 200 TPS 只作为配置声明，
   不实例化真实大张量，纯 Python 跑得动。

## 可复用思路

- 把「复杂任务」建模成 **子目标序列 + 工具链 + 动作接地** 三层，而不是一个黑盒端到端。
- 用 **确定性 oracle** 而不是随机数做基准，才能验证「训练确实提升了能力」。
- 用 **思考预算（thinking budget）** 按步衰减分配，模拟 flash 模型的性价比逻辑。
