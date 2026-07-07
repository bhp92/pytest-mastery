# exercises/03_week1_day3.py
#
# ╔══════════════════════════════════════════════════════════════╗
# ║  PYTEST MASTERY — Week 1, Day 3 Exercise                     ║
# ║  Topic: Assertions Deep Dive                                 ║
# ╚══════════════════════════════════════════════════════════════╝
#
# HOW TO RUN:
#   From the repo root:
#       pytest exercises/week1_day3.py -v
#
#   To see the rich assertion diff pytest generates on failure:
#       pytest exercises/week1_day3.py -v --tb=short
#
#   To stop on first failure:
#       pytest exercises/week1_day3.py -v -x
#
# GOAL: All 4 tasks + bonus should PASS when you're done.
# Do the tasks IN ORDER — Task 3 depends on the exception message
# format you notice in Task 2. Predict before you run.
# ──────────────────────────────────────────────────────────────

import warnings
import pytest


# ── SOURCE FUNCTIONS (do not edit these) ───────────────────────

def withdraw(balance: float, amount: float) -> float:
    """
    Withdraw `amount` from `balance`. Returns the new balance.
    Raises ValueError if amount is not positive.
    Raises ValueError if amount exceeds balance (insufficient funds).
    """
    if amount <= 0:
        raise ValueError(f"Withdrawal amount must be positive, got {amount}")
    if amount > balance:
        raise ValueError(
            f"Insufficient funds: balance is {balance}, requested {amount}"
        )
    return round(balance - amount, 2)


def build_profile(name: str, age: int) -> dict:
    """Return a user profile dict. Raises ValueError if age is negative."""
    if age < 0:
        raise ValueError(f"Age cannot be negative, got {age}")
    return {"name": name, "age": age, "active": True}


def legacy_get_balance(account: dict) -> float:
    """
    Deprecated: use account['balance'] directly instead.
    Emits a DeprecationWarning every time it's called.
    """
    warnings.warn(
        "legacy_get_balance() is deprecated, access account['balance'] directly",
        DeprecationWarning,
        stacklevel=2,
    )
    return account["balance"]


# ──────────────────────────────────────────────────────────────
# TASK 1 — Basic exception assertion
# ──────────────────────────────────────────────────────────────
# Write a test called `test_withdraw_zero_amount_raises` that verifies:
#   - Calling withdraw(100, 0) raises a ValueError
#
# Use pytest.raises as a context manager. No `match=` needed yet.

# YOUR CODE HERE
def test_withdraw_zero_amount_raises():
    with pytest.raises(ValueError):
        withdraw(100, 0)


# ──────────────────────────────────────────────────────────────
# TASK 2 — pytest.raises with match=
# ──────────────────────────────────────────────────────────────
# Write a test called `test_withdraw_insufficient_funds_message` that
# verifies BOTH of:
#   - withdraw(50, 100) raises a ValueError
#   - the exception message matches the regex pattern containing the
#     word "Insufficient"
#
# Remember: match= uses re.search, not re.match — it doesn't need to
# anchor at the start of the string.

# YOUR CODE HERE
def test_withdraw_insufficient_funds_message():
    with pytest.raises(ValueError, match=r"Insufficient"):
        withdraw(50, 100)

# ──────────────────────────────────────────────────────────────
# TASK 3 — Inspecting exc_info after the block
# ──────────────────────────────────────────────────────────────
# Write a test called `test_build_profile_negative_age_exc_info` that:
#   - Calls build_profile("Bob", -5) inside a pytest.raises(ValueError)
#     block, capturing the result as `exc_info`
#   - AFTER the `with` block, asserts that the string "-5" appears
#     somewhere in str(exc_info.value)
#   - AFTER the `with` block, asserts that exc_info.type is ValueError
#
# Think about why these assertions must be OUTSIDE the `with` block,
# not inside it. Write your answer as a one-line comment above the test.

# YOUR CODE HERE
def test_build_profile_negative_age_exc_info():
    with pytest.raises(ValueError) as exc_info:
        build_profile("Bob", -5)
    assert "-5" in str(exc_info.value)
    assert exc_info.type is ValueError

# ──────────────────────────────────────────────────────────────
# TASK 4 — pytest.warns
# ──────────────────────────────────────────────────────────────
# Write a test called `test_legacy_get_balance_warns` that verifies:
#   - Calling legacy_get_balance({"balance": 250}) emits a
#     DeprecationWarning
#   - The warning message matches a pattern containing the word
#     "deprecated"
#   - The function's return value is still checked as equal to 250
#     (i.e. prove the warning fires AND the function still works)

# YOUR CODE HERE
def test_legacy_get_balance_warns():
    with pytest.warns(DeprecationWarning, match=r"deprecated") as exc_info:
        result = legacy_get_balance({"balance": 250})
    assert result == 250

# ──────────────────────────────────────────────────────────────
# BONUS — Spot and fix the anti-pattern
# ──────────────────────────────────────────────────────────────
# The test below is BROKEN in a subtle way: it will pass, but not for
# the reason you'd think. Read it carefully.
#
#   def test_broken_withdraw_check():
#       with pytest.raises(ValueError):
#           build_profile("Eve", -1)   # raises here...
#           withdraw(50, 100)          # ...so this line NEVER runs
#
# Rewrite it below as `test_withdraw_insufficient_funds_isolated` so it
# actually tests what its name claims: that withdraw(50, 100) raises
# ValueError. Isolate exactly one call per pytest.raises block.
#
# Then, as a comment, explain in one sentence why the broken version
# would give you false confidence in a real codebase.
# Reason: pytest.raises (and try/except) only protect the first raising 
# line in a block — anything after it is dead code the moment an earlier
#  line raises. Always isolate one call per assertion block, or you're testing nothing.

# YOUR CODE HERE
def test_withdraw_insufficient_funds_isolated():
    with pytest.raises(ValueError):
        build_profile("Eve", -1)
    with pytest.raises(ValueError):
        withdraw(50, 100)