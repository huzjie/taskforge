# -*- coding: utf-8 -*-
"""Configuration for taskforge.

YAML is read through the bundled minimal parser (utils.yamlish) so the package
stays zero-dependency even when PyYAML is absent. PyYAML is preferred if present.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


def _load_yaml(text: str) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        from .utils.yamlish import parse
        return parse(text)


@dataclass
class PlannerConfig:
    max_steps: int = 32
    react_max_iters: int = 16
    decompose_mode: str = "dag"          # dag | linear
    thinking_budget: int = 2048          # thinking tokens per goal


@dataclass
class ToolsConfig:
    max_calls: int = 64
    retries: int = 3
    rollback: bool = True
    validate_results: bool = True


@dataclass
class GuiConfig:
    screen_w: int = 1280
    screen_h: int = 800
    n_elements: int = 12
    action_set: List[str] = field(default_factory=lambda: [
        "click", "type", "scroll", "press", "drag", "hover",
    ])


@dataclass
class SparseConfig:
    block_size: int = 16
    top_k: int = 4
    dim: int = 32
    seq_len: int = 128


@dataclass
class MemoryConfig:
    capacity: int = 256
    stall_threshold: int = 3
    recovery_budget: int = 5


@dataclass
class ModelConfig:
    backend: str = "mock"
    temperature: float = 0.0
    model_id: str = "taskforge-mock"


@dataclass
class BenchConfig:
    n_tasks: int = 64
    n_seen: int = 32
    n_unseen: int = 32
    episodes: int = 4
    horizon: int = 8


@dataclass
class Config:
    planner: PlannerConfig = field(default_factory=PlannerConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    gui: GuiConfig = field(default_factory=GuiConfig)
    sparse: SparseConfig = field(default_factory=SparseConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    bench: BenchConfig = field(default_factory=BenchConfig)
    # declared scale (informational; not instantiated as real tensors)
    total_params_b: float = 560.0
    active_params_b: float = 25.0
    context_window: int = 1000000
    tokens_per_second: int = 200

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Config":
        cfg = cls()
        if not d:
            return cfg
        for section in ("planner", "tools", "gui", "sparse", "memory", "model", "bench"):
            if section in d and isinstance(d[section], dict):
                sub = getattr(cfg, section)
                for k, v in d[section].items():
                    if hasattr(sub, k):
                        setattr(sub, k, v)
        for k in ("total_params_b", "active_params_b", "context_window", "tokens_per_second"):
            if k in d:
                setattr(cfg, k, d[k])
        return cfg

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def load_config(path: Optional[str] = None) -> Config:
    if path is None:
        here = Path(__file__).resolve().parent
        path = str(here / "configs" / "default.yaml")
    p = Path(path)
    if p.exists():
        data = _load_yaml(p.read_text(encoding="utf-8"))
        return Config.from_dict(data)
    return Config()


def default_config() -> Config:
    return Config()
