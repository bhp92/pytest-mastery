"""
Week 1: Foundations
Run with: pytest week1/test_foundations.py -v
"""
import pytest


# ── Day 1: Basic assertions ────────────────────────────────────────────────

def test_addition():
    assert 1 + 1 == 2


def test_string_contains():
    result = "Hello, pytest!"
    assert "pytest" in result


def test_list_length():
    items = [1, 2, 3]
    assert len(items) == 3


# ── Day 3: pytest.raises ───────────────────────────────────────────────────

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def test_divide_normal():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)


def test_raises_captures_exception_info():
    with pytest.raises(ValueError) as exc_info:
        divide(5, 0)
    assert "zero" in str(exc_info.value)


# ── Day 3: pytest.warns ────────────────────────────────────────────────────

import warnings

def legacy_function():
    warnings.warn("This function is deprecated", DeprecationWarning)
    return 42


def test_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        result = legacy_function()
    assert result == 42


# ── Day 4: Marks ───────────────────────────────────────────────────────────

@pytest.mark.slow
def test_slow_operation():
    """Marked slow — skipped unless --slow passed (see conftest.py)"""
    import time
    time.sleep(0.1)
    assert True


@pytest.mark.unit
def test_fast_unit():
    assert 2 ** 10 == 1024


# ── Day 4: skip / skipif ───────────────────────────────────────────────────

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    assert False  # Will never run


import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_only_behavior():
    import os
    assert os.sep == "/"


# ── Day 3: xfail ──────────────────────────────────────────────────────────

@pytest.mark.xfail(reason="Known bug #42 — fix in progress")
def test_known_broken():
    assert 1 == 2  # expected to fail


@pytest.mark.xfail(strict=True, reason="Must fix before release")
def test_must_be_fixed():
    # Change this to `assert True` and re-run — strict=True means
    # an unexpected PASS is a CI failure until you remove the mark
    assert False
