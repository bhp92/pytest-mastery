# exercises/week1_day1.py
#
# ╔══════════════════════════════════════════════════════════════╗
# ║  PYTEST MASTERY — Week 1, Day 1 Exercise                    ║
# ║  Topic: Install & First Test                                 ║
# ╚══════════════════════════════════════════════════════════════╝
#
# HOW TO RUN:
#   From the repo root:
#       pytest exercises/week1_day1.py -v
#
#   To stop on first failure:
#       pytest exercises/week1_day1.py -v -x
#
#   To see print() output:
#       pytest exercises/week1_day1.py -v -s
#
# GOAL: All 4 tasks + bonus should PASS when you're done.
# ──────────────────────────────────────────────────────────────


# ── SOURCE FUNCTIONS (do not edit these) ──────────────────────

def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit. Formula: (c * 9/5) + 32"""
    return (c * 9 / 5) + 32


def get_discount(price, member: bool):
    """
    Return the final price after discount.
    Members get 20% off. Non-members get 5% off.
    Raises ValueError if price is negative.
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    discount = 0.20 if member else 0.05
    return round(price * (1 - discount), 2)


def repeat_string(s, n):
    """Return string s repeated n times. Returns '' if n <= 0."""
    if n <= 0:
        return ""
    return s * n


# ──────────────────────────────────────────────────────────────
# TASK 1 — Basic assertion
# ──────────────────────────────────────────────────────────────
# Write a test called `test_freezing_point` that verifies:
#   - celsius_to_fahrenheit(0) equals 32.0
#
# Hint: just use a bare `assert`

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 2 — Multiple assertions in one test
# ──────────────────────────────────────────────────────────────
# Write a test called `test_boiling_and_body_temp` that verifies:
#   - celsius_to_fahrenheit(100) equals 212.0
#   - celsius_to_fahrenheit(37) equals 98.6
#
# Both assertions must be in the SAME test function.

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 3 — Testing branches (member vs non-member)
# ──────────────────────────────────────────────────────────────
# Write TWO separate tests:
#   - `test_member_discount`: price=100, member=True  → expects 80.0
#   - `test_nonmember_discount`: price=100, member=False → expects 95.0

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 4 — Testing that an exception is raised
# ──────────────────────────────────────────────────────────────
# Write a test called `test_negative_price_raises` that verifies:
#   - Calling get_discount(-10, True) raises a ValueError
#   - The error message contains the word "negative"
#
# You MUST use pytest.raises as a context manager.
# Import pytest at the top of the function (or at file level — your choice).

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# BONUS — Edge cases & type precision
# ──────────────────────────────────────────────────────────────
# Write a test called `test_repeat_string_edge_cases` that verifies ALL of:
#   - repeat_string("ha", 3)  == "hahaha"
#   - repeat_string("hi", 0)  == ""
#   - repeat_string("hi", -5) == ""
#   - The return type is always `str` (check all three results with isinstance)
#
# Think: why does type-checking matter here at a senior level?
# (Write your answer as a comment above the test)

# YOUR CODE HERE