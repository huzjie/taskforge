# -*- coding: utf-8 -*-
import unittest

from taskforge.tools.registry import ToolRegistry
from taskforge.tools.schema import ToolSchema


class TestRegistry(unittest.TestCase):
    def test_get_and_names(self):
        reg = ToolRegistry()
        names = reg.names()
        self.assertIn("browser.open", names)
        self.assertEqual(reg.get("browser.open").name, "browser.open")

    def test_schema_json(self):
        s = ToolSchema(name="x", description="d", parameters={"a": "string"}, required=["a"])
        js = s.json_schema()
        self.assertEqual(js["function"]["name"], "x")


if __name__ == "__main__":
    unittest.main()
