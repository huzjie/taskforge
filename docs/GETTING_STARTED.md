# 快速上手

```bash
# 1. 冒烟自检（5 后端 + 规划/工具/接地/稀疏 + 引擎端到端）
python -m taskforge doctor

# 2. 训练 + 全基准
python -m taskforge bench

# 3. 单目标工作流
python -m taskforge run --goal goal-0

# 4. 起 HTTP 服务
python -m taskforge serve --host 127.0.0.1 --port 8787
```

HTTP 端点：`GET /health`、`GET /v1/models`、`POST /v1/plan`、`POST /v1/run`、`POST /v1/ground`。

Docker：

```bash
docker compose -f deploy/docker-compose.yml up --build
```
