# FAQ

**Q: 为什么要零依赖？**
A: 参考实现要能在任何 Python 3.12 直接跑，不装 numpy/pyyaml/requests；
   内置 `yamlish` 与 `stable` 兜底，有 PyYAML 时优先用之。

**Q: 基准数字是真的吗？**
A: 是。所有数字由 `python -m taskforge bench` 实时测量，README 表格与代码输出一致。

**Q: 如何接入真实模型？**
A: 继承 `model/backends.py` 的 `_BaseBackend`，实现 `plan/choose_tool/ground/think/next_token`，
   用 `@register_backend("my-model")` 注册即可。
