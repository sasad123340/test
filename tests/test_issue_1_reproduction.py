"""
Reproduction tests for GitHub Issue #1: hello.py has a bug

These tests assert the CORRECT/expected behavior of hello.py.
They will FAIL on the current buggy code and PASS once the bug is fixed.

Bugs in hello.py:
1. Unclosed string literal on line 2 (SyntaxError prevents execution)
2. Typo: "Helo" should be "Hello"
3. Unused `name` parameter — greet(name) should use `name` in its output
"""

import unittest
import importlib
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestIssue1Reproduction(unittest.TestCase):
    """Tests that hello.py greet() works correctly once fixed."""

    def test_hello_module_imports_without_error(self):
        """The module should be importable without a SyntaxError."""
        try:
            import hello
            importlib.reload(hello)
        except SyntaxError:
            self.fail("hello.py raises SyntaxError on import (unclosed string literal)")

    def test_greet_returns_string(self):
        """greet() should return a string."""
        import hello
        importlib.reload(hello)
        result = hello.greet("World")
        self.assertIsInstance(result, str)

    def test_greet_contains_hello(self):
        """greet() should say 'Hello', not 'Helo'."""
        import hello
        importlib.reload(hello)
        result = hello.greet("World")
        self.assertIn("Hello", result, "Expected 'Hello' but got a typo like 'Helo'")

    def test_greet_uses_name_parameter(self):
        """greet(name) should include the provided name in the output."""
        import hello
        importlib.reload(hello)
        result = hello.greet("Alice")
        self.assertIn("Alice", result, "The name parameter should appear in the greeting")

    def test_greet_full_output(self):
        """greet('World') should return 'Hello World' (or similar greeting with the name)."""
        import hello
        importlib.reload(hello)
        result = hello.greet("World")
        self.assertEqual(result, "Hello World")


if __name__ == "__main__":
    unittest.main()
