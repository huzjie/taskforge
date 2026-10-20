# 配方：切换后端

```python
from taskforge.config import Config
from taskforge.model.backends import get_backend, list_backends
print(list_backends())
b = get_backend("openai", Config())
```

要点：后端实现同一接口，切后端不改业务代码。
