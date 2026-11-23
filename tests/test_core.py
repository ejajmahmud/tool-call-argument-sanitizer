"""Tests for ToolCallSanitizer."""
import unittest
from tool_call_argument_sanitizer.core import ToolCallSanitizer

class TestToolCallSanitizer(unittest.TestCase):
    def test_path_and_shell_injection(self):
        schema = {"path": {"type": "string"}}
        raw = {"path": "../../../bin/bash | echo bad"}
        res = ToolCallSanitizer.sanitize(raw, schema)
        self.assertNotIn("../", res.sanitized_args["path"])
        self.assertNotIn("|", res.sanitized_args["path"])

    def test_type_coercion(self):
        schema = {"limit": {"type": "integer"}, "flag": {"type": "boolean"}}
        raw = {"limit": "42", "flag": "yes", "unknown": "junk"}
        res = ToolCallSanitizer.sanitize(raw, schema)
        self.assertEqual(res.sanitized_args["limit"], 42)
        self.assertEqual(res.sanitized_args["flag"], True)
        self.assertNotIn("unknown", res.sanitized_args)
