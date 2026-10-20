# 贡献指南

1. 改动后先跑 `python -m compileall -q taskforge`。
2. 再跑 `python -m unittest discover -s taskforge/tests -t .`。
3. 新增后端/基准请用 `@register_backend` / `@register_benchmark` 并显式 import。
4. README 的基准数字必须来自 `python -m taskforge bench` 实测。
