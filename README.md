# taskforge — 复杂长程智能体工作流编排引擎

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)](.github/workflows/ci.yml)
[![Zero-dependency](https://img.shields.io/badge/deps-zero-lightgrey)](pyproject.toml)

> 零依赖的**长程智能体工作流编排引擎**参考实现，把 MiniMax M3.1 Flash「太空兔」在复杂
> Agent 任务上的能力拆成五个可复用工程件：**多步规划、连续工具调用、电脑操作（GUI）动作接地、
> 长程工作记忆、稀疏注意力推理加速**。填好配置、`python -m taskforge` 即可完整跑通。

---

## 技术原理拆解

M3.1 Flash 能拿下 AutomationBench 全场第一、OSWorld 61.7、DeepSWE 73.7，靠的不是更大参数，
而是**把「复杂长程任务」拆成三层可组合结构 + 一个省算力的推理路径**。taskforge 完整复刻这套思路：

### 1. 多步规划（planner）
自然语言目标 → 有序子目标 DAG。每个子目标必须对应一个明确工具动作，后步子目标依赖前步产出。
配合 `ThinkingBudget` 按步衰减分配思考 token，模拟 flash 模型的性价比逻辑。

### 2. 连续工具调用（tools）
每个子目标绑定「工具 schema + 参数 + 结果校验 + 重试/回滚」，让一条链从头跑到尾，
单步失败不中断整条链。

### 3. 电脑操作动作接地（gui）
屏幕建模成「UI 元素树」而非原始像素，把自然语言意图接地为 `(element_id, action)` 的离散选择，
跨应用状态机跟踪「现在在哪个 app」。

### 4. 长程工作记忆（memory）
20 步以上的工作流靠一个 scratchpad 记录进度；「连续失败计数」触发卡点恢复，而非单次失败。

### 5. 稀疏注意力加速（sparse）
索引分支低秩打分 O(n·rank) 选出 top-k 块，稀疏分支只对这些块做 softmax，
加速比 ≈ `n_blocks / top_k`。

---

## 快速开始

```bash
# 冒烟自检（5 后端 + 规划/工具/接地/稀疏 + 引擎端到端）
python -m taskforge doctor

# 训练 + 全基准
python -m taskforge bench

# 单目标工作流
python -m taskforge run --goal goal-0

# HTTP 服务
python -m taskforge serve --host 127.0.0.1 --port 8787
```

Docker：

```bash
docker compose -f deploy/docker-compose.yml up --build
```

## 基准（实测，`python -m taskforge bench`）

> 数值由 mock 后端实时测量；`skill = 0.5` 为随机基线、`skill = 1.0` 为满分。

| 基准 | 含义 | skill=0.5 | skill=1.0 |
| --- | --- | --- | --- |
| planning | 多步规划成功率 | 0.094 | 1.00 |
| tools | 工具链准确率 | 0.556 | 1.00 |
| gui | GUI 动作接地准确率 | 0.453 | 1.00 |
| sparse | 黄金块召回率（加速比 2.0×） | 0.497 | 1.00 |
| longhorizon | 长程完成率（horizon=8） | 0.0 | 1.00 |

长程任务卡点恢复的价值（`skill=0.8`）：无恢复完成率 **0.25** → 有恢复 **0.8125**（约 3.25×）。

## 实现思路（可复用要点）

1. **单一真值 oracle**：mock 后端与所有基准共享同一确定性真值，训练是否有效可被严格验证。
2. **单调训练信号**：`boost = (skill - 0.5) * 2`，skill=0.5 时 boost 恰为 0（随机基线）、
   skill=1.0 恒正确；绝不用「对 +1 / 错 -1」的随机游走。
3. **声明规模与实例化解耦**：560B 总参 / 25B 激活 / 1M 上下文 / 200 TPS 只作配置声明，
   不实例化真实大张量，纯 Python 跑得动。
4. **确定性随机**：`md5(key)` 前 8 字节做种子驱动 `random.Random`，任何 key 输出可复现。

## 项目结构

```
taskforge/
  planner/    多步规划 + ReAct + 思考预算
  tools/      工具 schema + 注册表 + 编排器
  gui/        屏幕模型 + 动作接地 + 状态机
  memory/     工作记忆 + 卡点检测
  sparse/     稀疏注意力 + 分块路由
  model/      5 后端（mock/openai/vllm/transformers/anthropic）
  bench/      5 基准（planning/tools/gui/sparse/longhorizon）
  serving/    HTTP 服务 + CLI
  utils/      yamlish / stable / hashing
  tests/      单元测试
examples/    9 个可运行示例
docs/        架构 / API / 快速上手
prompts/     5 个提示词模板
recipes/     4 个可复用配方
deploy/      Docker / K8s / Helm / CI
```

## License

[MIT](LICENSE)
