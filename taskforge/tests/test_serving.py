# -*- coding: utf-8 -*-
import unittest

from taskforge.config import Config
from taskforge.serving.server import _load


class TestServing(unittest.TestCase):
    def test_load_json(self):
        self.assertEqual(_load(b'{"a": 1}'), {"a": 1})

    def test_load_empty(self):
        self.assertEqual(_load(b""), {})

    def test_load_bad_json(self):
        self.assertEqual(_load(b"{bad"), {})


if __name__ == "__main__":
    unittest.main()
