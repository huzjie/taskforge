# taskforge - long-horizon agent workflow orchestration engine
FROM python:3.12-slim

WORKDIR /app

# zero runtime dependencies
COPY taskforge/ ./taskforge/
COPY README.md LICENSE pyproject.toml ./

ENV PYTHONUNBUFFERED=1

EXPOSE 8787

CMD ["python", "-m", "taskforge", "serve", "--host", "0.0.0.0", "--port", "8787"]
