# week1_day1_example.py
# Run with: pytest week1_day1_example.py -v

# ── The function we want to test ─────────────────────────────────────────────

def add(a, b):
    """Add two numbers. Simple, but illustrates every pytest concept."""
    return a + b


def divide(a, b):
    """Divide a by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def is_even(n):
    """Return True if n is even, False otherwise."""
    return n % 2 == 0


# ── Tests ────────────────────────────────────────────────────────────────────
# pytest discovers these because:
#   1. The file is named test_*.py (or we run it directly)
#   2. Each function starts with test_

def test_add_two_positive_numbers():
    # Bare assert — pytest rewrites this to show both sides on failure
    assert add(2, 3) == 5


def test_add_negative_numbers():
    # Testing an edge case: negatives
    assert add(-1, -1) == -2


def test_add_returns_int_not_float():
    # Be precise: int + int should stay int
    result = add(1, 2)
    assert isinstance(result, int), f"Expected int, got {type(result)}"


def test_divide_normal_case():
    assert divide(10, 2) == 5.0


def test_divide_by_zero_raises():
    # pytest.raises is a context manager that *expects* an exception.
    # If the exception is NOT raised, the test FAILS.
    import pytest
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_divide_by_zero_checks_message():
    # Senior level: also assert the exception *message* when it matters
    import pytest
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        divide(10, 0)


def test_is_even_returns_bool_not_int():
    # BEGINNER TRAP: n % 2 == 0 returns True/False in Python (bool),
    # but if someone rewrites it as `return not n % 2`, it still works
    # for truthiness but returns an int (0 or 1). Be explicit.
    result = is_even(4)
    assert result is True          # `assert result` would also pass for int 1
    assert isinstance(result, bool)


def test_is_even_false_case():
    assert is_even(3) is False


# ── What a FAILING test looks like ───────────────────────────────────────────
# Uncomment to see pytest's output rewriting in action:
#
# def test_intentional_failure():
#     assert add(2, 2) == 5
#
# pytest will print:
#   AssertionError: assert 4 == 5
#    +  where 4 = add(2, 2)