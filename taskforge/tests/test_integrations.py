# -*- coding: utf-8 -*-
import unittest

from taskforge.integrations.langchain import to_langchain_tools
from taskforge.integrations.openai_fns import to_openai_functions


class TestIntegrations(unittest.TestCase):
    def test_langchain_tools(self):
        tools = to_langchain_tools()
        self.assertGreater(len(tools), 5)

    def test_openai_functions(self):
        fns = to_openai_functions()
        self.assertGreater(len(fns), 5)
        self.assertIn("function", fns[0])


if __name__ == "__main__":
    unittest.main()
