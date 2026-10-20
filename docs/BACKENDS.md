# 后端接入

统一接口见 `model/backends.py`，五个后端：

| 后端 | 说明 |
| --- | --- |
| mock | 确定性、可训练（skill 0.5 → 1.0），默认 |
| openai | 委托 mock 核心，换 SDK 即可接生产 |
| vllm | 同上 |
| transformers | 同上 |
| anthropic | 同上 |

接入真实模型：继承 `_BaseBackend`，实现 `plan/choose_tool/ground/think/next_token`，
用 `@register_backend("my-model")` 注册，`from . import my_model` 触发注册即可。
