# -*- coding: utf-8 -*-
import unittest

from taskforge.utils.yamlish import parse


class TestYamlish(unittest.TestCase):
    def test_scalars(self):
        d = parse("a: 1\nb: hello\nc: true\nd: 2.5\n")
        self.assertEqual(d["a"], 1)
        self.assertEqual(d["b"], "hello")
        self.assertEqual(d["c"], True)
        self.assertEqual(d["d"], 2.5)

    def test_nested(self):
        d = parse("model:\n  backend: mock\n  temperature: 0.0\n")
        self.assertEqual(d["model"]["backend"], "mock")

    def test_block_list(self):
        d = parse("action_set:\n  - click\n  - type\n  - scroll\n")
        self.assertEqual(d["action_set"], ["click", "type", "scroll"])

    def test_inline_list(self):
        d = parse("xs: [1, 2, 3]\n")
        self.assertEqual(d["xs"], [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
