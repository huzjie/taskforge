# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config, load_config, default_config


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        cfg = Config()
        self.assertEqual(cfg.model.backend, "mock")
        self.assertEqual(cfg.sparse.top_k, 4)
        self.assertEqual(cfg.planner.react_max_iters, 16)

    def test_from_dict(self):
        cfg = Config.from_dict({"model": {"backend": "openai"}, "tokens_per_second": 250})
        self.assertEqual(cfg.model.backend, "openai")
        self.assertEqual(cfg.tokens_per_second, 250)

    def test_load_default_yaml(self):
        cfg = load_config()
        self.assertEqual(cfg.model.backend, "mock")
        self.assertGreater(cfg.total_params_b, 0)

    def test_default_config(self):
        self.assertIsInstance(default_config(), Config)


if __name__ == "__main__":
    unittest.main()
