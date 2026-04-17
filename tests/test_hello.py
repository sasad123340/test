"""
Tests for GitHub Issue #1: hello.py has a bug

Verifies that hello.py's greet() function:
1. Can be imported without SyntaxError (unclosed string literal fix)
2. Returns greeting with correct "Hello" spelling (not "Helo")
3. Incorporates the name parameter in output
4. Produces different output for different names (name not hardcoded)
5. Runs as a script without errors via subprocess

All tests FAIL on the current buggy code and PASS once the bug is fixed.
"""

import importlib
import subprocess
import sys
import os

import pytest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def _load_hello():
    """Import (or reload) hello module to get fresh state."""
    import hello
    importlib.reload(hello)
    return hello


# Test 1: Module imports and greet() is callable without errors
def test_module_imports_and_greet_callable():
    """hello.py should import without SyntaxError and greet() should return a value."""
    hello = _load_hello()
    result = hello.greet("World")
    assert result is not None, "greet() should return a value, got None"


# Test 2: greet() returns greeting with correct "Hello" spelling
def test_greet_contains_hello_not_helo():
    """greet() should say 'Hello', not 'Helo'."""
    hello = _load_hello()
    result = hello.greet("World")
    assert "Hello" in result, f"Expected 'Hello' in greeting but got: {result!r}"


# Test 3: greet() incorporates the name parameter in output
def test_greet_uses_name_parameter():
    """greet('Alice') should include 'Alice' in the output."""
    hello = _load_hello()
    result = hello.greet("Alice")
    assert "Alice" in result, f"Expected 'Alice' in greeting but got: {result!r}"


# Test 4: greet() produces different output for different names
def test_greet_different_names_produce_different_output():
    """greet('Alice') and greet('Bob') should return different results."""
    hello = _load_hello()
    result_alice = hello.greet("Alice")
    result_bob = hello.greet("Bob")
    assert result_alice != result_bob, (
        f"Different names should produce different greetings, "
        f"but both returned: {result_alice!r}"
    )


# Test 5: Script execution via subprocess produces no errors
def test_script_runs_without_syntax_error():
    """Running hello.py as a script should not produce a SyntaxError."""
    hello_path = os.path.join(os.path.dirname(__file__), "..", "hello.py")
    result = subprocess.run(
        [sys.executable, hello_path],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, (
        f"hello.py exited with code {result.returncode}. stderr: {result.stderr}"
    )
    assert "SyntaxError" not in result.stderr, (
        f"hello.py has a SyntaxError: {result.stderr}"
    )
