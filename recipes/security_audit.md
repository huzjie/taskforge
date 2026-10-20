# 配方：代码安全审计

```python
from taskforge.security.audit import audit_code
r = audit_code("os.system('rm -rf /')", skill=1.0)
print(r["flags"])   # ['os.system']
```

要点：风险模式是**固定真值集**，skill 高时必然命中、skill 低时随机漏报。
