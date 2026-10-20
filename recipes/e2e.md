# 配方：端到端 HTTP 服务

```bash
python -m taskforge serve --port 8787 &
curl http://127.0.0.1:8787/health
curl -X POST http://127.0.0.1:8787/v1/run -d '{"goal_id":"goal-0"}'
```

要点：服务零依赖 stdlib `http.server`，`/v1/run` 返回完整工作流结果。
