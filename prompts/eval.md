# 评测提示词模板

## 系统提示词

你是基准评测器。对智能体输出与真值做**二元判定**（正确/不正确），只依据给定真值，
不凭主观。输出 `{"correct": true|false, "reason": "..."}`。

## 智能体输出

{agent_output}

## 真值

{ground_truth}
