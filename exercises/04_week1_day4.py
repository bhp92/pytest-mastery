# exercises/04_week1_day4.py
#
# ╔══════════════════════════════════════════════════════════════╗
# ║  PYTEST MASTERY — Week 1, Day 4 Exercise                     ║
# ║  Topic: Running Tests Selectively                            ║
# ╚══════════════════════════════════════════════════════════════╝
#
# HOW TO RUN:
#   From the repo root:
#       pytest exercises/04_week1_day4.py -v
#
#   Once you've added markers, try these (do this AFTER Task 2):
#       pytest exercises/04_week1_day4.py -m "unit" -v
#       pytest exercises/04_week1_day4.py -m "slow" -v
#       pytest exercises/04_week1_day4.py -m "not slow" -v
#       pytest exercises/04_week1_day4.py -k "discount" -v
#       pytest exercises/04_week1_day4.py -k "discount and not negative" -v
#       pytest exercises/04_week1_day4.py -x
#       pytest exercises/04_week1_day4.py --tb=short
#       pytest exercises/04_week1_day4.py -s
#
# GOAL: All 4 tasks + bonus should PASS when you're done.
# Do the tasks IN ORDER — Task 3 depends on markers you register
# in Task 2, and the bonus depends on registering a NEW marker
# that isn't in pytest.ini yet.
# ──────────────────────────────────────────────────────────────

import pytest


# ── SOURCE FUNCTIONS (do not edit these) ───────────────────────

def apply_discount(price: float, percent: float) -> float:
    """
    Apply a percentage discount to a price.
    Raises ValueError if percent is not between 0 and 100.
    """
    if not (0 <= percent <= 100):
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    return round(price * (1 - percent / 100), 2)


def process_large_order(items: list) -> float:
    """
    Pretend this hits a real payment gateway — deliberately slow
    to simulate expensive I/O in a real test suite.
    """
    import time
    time.sleep(0.2)
    return round(sum(items), 2)


def sync_inventory_with_warehouse(sku: str) -> str:
    """
    Pretend this calls a real external warehouse API.
    In a real suite this would be marked @pytest.mark.integration
    and skipped in fast local runs.
    """
    return f"synced:{sku}"


# ──────────────────────────────────────────────────────────────
# TASK 1 — Write two plain tests (no markers yet)
# ──────────────────────────────────────────────────────────────
# Write a test called `test_apply_discount_ten_percent` that verifies:
#   - apply_discount(200, 10) == 180.0
#
# Write a second test called `test_apply_discount_invalid_percent_raises`
# that verifies:
#   - Calling apply_discount(100, 150) raises a ValueError
#
# Run `pytest exercises/04_week1_day4.py -v` and confirm both pass.

# YOUR CODE HERE
@pytest.mark.unit
def test_apply_discount_ten_percent():
    assert apply_discount(200, 10) == 180.0

def test_apply_discount_invalid_percent_raises():
    with pytest.raises(ValueError):
        apply_discount(100, 150)

# ──────────────────────────────────────────────────────────────
# TASK 2 — Add markers
# ──────────────────────────────────────────────────────────────
# Decorate `test_apply_discount_ten_percent` from Task 1 with
# @pytest.mark.unit
#
# Write a NEW test called `test_process_large_order_total` that:
#   - Decorate it with @pytest.mark.slow
#   - Calls process_large_order([10.50, 20.25, 5.00])
#   - Asserts the result equals 35.75
#
# Both `unit` and `slow` are already registered in the repo's
# pytest.ini — check that file if you're unsure of the exact names.
#
# Run:
#   pytest exercises/04_week1_day4.py -m "unit" -v
#   pytest exercises/04_week1_day4.py -m "slow" -v
# and confirm each command runs ONLY the test you'd expect.

# YOUR CODE HERE

@pytest.mark.slow
def test_process_large_order_total():
    assert process_large_order([10.50, 20.25, 5.00]) == 35.75

# ──────────────────────────────────────────────────────────────
# TASK 3 — Combine -k and -m in your head, then verify
# ──────────────────────────────────────────────────────────────
# Write a test called `test_apply_discount_zero_percent` that verifies:
#   - apply_discount(50, 0) == 50.0
# Mark it @pytest.mark.unit
#
# Before running anything, write a one-line comment predicting how
# many tests each of these commands will select, given everything
# you've written in Tasks 1-3:
#   pytest exercises/04_week1_day4.py -k "discount" -v                  # 3 tests will run
#   pytest exercises/04_week1_day4.py -m "unit" -k "not invalid" -v     # 2 tests will run
#
# THEN run them and check your prediction was correct. If it wasn't,
# figure out why before moving on — don't just shrug and continue.

# YOUR CODE HERE

@pytest.mark.unit
def test_apply_discount_zero_percent():
    assert apply_discount(50, 0) == 50.0

# ──────────────────────────────────────────────────────────────
# TASK 4 — Register and use a brand-new marker
# ──────────────────────────────────────────────────────────────
# The `integration` marker already exists in pytest.ini, but let's
# practice registering one from scratch conceptually: add a comment
# explaining what line you'd add to pytest.ini to register a marker
# called `external_api` (don't actually edit pytest.ini for this
# exercise — just write the line as a comment).
#
# I would create a marker under markers section in pytest.ini. <marker>: <comment>
#
# Then write a test called `test_sync_inventory_with_warehouse` that:
#   - Decorate it with @pytest.mark.integration (this one IS
#     already registered, so it's safe to use for real)
#   - Calls sync_inventory_with_warehouse("SKU-123")
#   - Asserts the result equals "synced:SKU-123"
#
# Run pytest exercises/04_week1_day4.py -m "integration" -v
# and confirm only this test runs.

# YOUR CODE HERE

@pytest.mark.integration
def test_sync_inventory_with_warehouse():
    assert sync_inventory_with_warehouse("SKU-123") == "synced:SKU-123"

# ──────────────────────────────────────────────────────────────
# BONUS — Diagnose a broken CI command
# ──────────────────────────────────────────────────────────────
# A teammate says their CI stage runs:
#
#     pytest -m "unit or slow" -x --tb=no
#
# ...and complains that when 3 unrelated tests are broken, CI only
# ever reports 1 failure, so they keep "fixing one thing at a time"
# across multiple pushes and it's wasting review cycles.
#
# As a comment below, answer:
#   1. Which flag is causing this behavior, and why?
#   2. What would you change this command to, for a CI stage
#      (as opposed to local dev), so a single push surfaces every
#      failing test at once?
#   3. Would you still recommend `-x` anywhere in this workflow?
#      If so, where?

# YOUR ANSWER HERE (as comments)
# -x makes sure that CI stops after hitting first failure
# Locally you want -x (stop fast, fix fast, tight loop). In CI you want 
# the opposite — maximum information per run, because a push is expensive 
# and round-trips are slow. --tb=no is for a quick pass/fail headcount 
# (e.g. a smoke-test dashboard), not for a stage a human will actually have to debug from.
