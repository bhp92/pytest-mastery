"""
Week 3: Parametrize & Marks
Run with: pytest week3/test_parametrize.py -v
"""
import pytest
import math


# ── Day 1: Basic parametrize ───────────────────────────────────────────────

def is_even(n):
    return n % 2 == 0


@pytest.mark.parametrize("number, expected", [
    (2,  True),
    (3,  False),
    (0,  True),
    (-4, True),
    (7,  False),
])
def test_is_even(number, expected):
    assert is_even(number) == expected


# ── Day 1: Multiple parameters ────────────────────────────────────────────

def add(a, b):
    return a + b


@pytest.mark.parametrize("a, b, expected", [
    (1,   2,   3),
    (0,   0,   0),
    (-1,  1,   0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected


# ── Day 2: pytest.param with per-case marks ────────────────────────────────

def safe_sqrt(n):
    if n < 0:
        raise ValueError(f"Cannot take sqrt of {n}")
    return math.sqrt(n)


@pytest.mark.parametrize("value, expected", [
    (4,   2.0),
    (9,   3.0),
    (0,   0.0),
    pytest.param(2, 1.414, id="irrational",    marks=pytest.mark.unit),
    pytest.param(-1, None,  id="negative-raises", marks=pytest.mark.xfail(raises=ValueError)),
])
def test_safe_sqrt(value, expected):
    assert round(safe_sqrt(value), 3) == expected


# ── Day 2: Cartesian product (stacked parametrize) ─────────────────────────

@pytest.mark.parametrize("base",     [2, 10])
@pytest.mark.parametrize("exponent", [0, 1, 2])
def test_power(base, exponent):
    """Runs 6 times: every combination of base × exponent."""
    result = base ** exponent
    assert result == pow(base, exponent)


# ── Day 3: skipif ─────────────────────────────────────────────────────────

import sys

@pytest.mark.parametrize("input_str, expected", [
    ("hello", "HELLO"),
    ("PyTest", "PYTEST"),
])
@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9+")
def test_upper(input_str, expected):
    assert input_str.upper() == expected


# ── Day 4: Custom marks (registered in pytest.ini) ────────────────────────

@pytest.mark.unit
def test_pure_logic():
    assert sorted([3, 1, 2]) == [1, 2, 3]


@pytest.mark.slow
def test_expensive_computation():
    """
    Run only with: pytest -m slow
    Skip with:     pytest -m "not slow"
    """
    total = sum(range(10_000_000))
    assert total == 49_999_995_000_000


# ── Day 5: Parametrize with indirect ──────────────────────────────────────

@pytest.fixture
def user_with_role(request):
    """Fixture receives role via request.param (indirect parametrize)."""
    role = request.param
    permissions = {
        "admin":  ["read", "write", "delete"],
        "editor": ["read", "write"],
        "viewer": ["read"],
    }
    return {"role": role, "permissions": permissions[role]}


@pytest.mark.parametrize("user_with_role, can_delete", [
    ("admin",  True),
    ("editor", False),
    ("viewer", False),
], indirect=["user_with_role"])
def test_delete_permission(user_with_role, can_delete):
    has_delete = "delete" in user_with_role["permissions"]
    assert has_delete == can_delete
