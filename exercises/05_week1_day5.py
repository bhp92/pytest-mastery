# exercises/05_week1_day5.py
#
# ╔══════════════════════════════════════════════════════════════╗
# ║  PYTEST MASTERY — Week 1, Day 5 Exercise                     ║
# ║  Topic: Organizing Test Files                                ║
# ╚══════════════════════════════════════════════════════════════╝
#
# HOW TO RUN:
#   From the repo root, this file should stay green on its own:
#       pytest exercises/05_week1_day5.py -v
#
#   Several tasks also ask you to run experiments in a THROWAWAY
#   directory. Do those in a scratch folder OUTSIDE the repo so you
#   don't pollute the suite, e.g.:
#       mkdir -p ~/pytest_scratch && cd ~/pytest_scratch
#
#   Useful commands you'll need today:
#       pytest --collect-only -q            # show what WOULD run, run nothing
#       pytest -q                           # default (prepend) import mode
#       pytest -q --import-mode=importlib   # modern import mode
#
# GOAL: All 4 tasks + bonus. The real tests in THIS file must PASS;
# the layout tasks are proven by (a) the pytest output you observe in
# your scratch dir and (b) the written answers you leave as comments.
#
# Do the tasks IN ORDER — each builds on the last:
#   Task 1: src-layout import behavior  (why `src/` forces an install)
#   Task 2: reproduce `import file mismatch` (duplicate basenames)
#   Task 3: fix it TWO ways and pick one (__init__.py vs importlib)
#   Task 4: conftest placement as an organizing decision (scope)
# ──────────────────────────────────────────────────────────────

import pytest


# ── SOURCE FUNCTIONS (do not edit these) ───────────────────────
# These exist so THIS file has something real to test while you
# practice the layout concepts in your scratch dir.

def apply_tax(price: float, rate: float) -> float:
    """
    Add a tax rate (e.g. 0.18 for 18%) to a price.
    Raises ValueError if rate is negative.
    """
    if rate < 0:
        raise ValueError(f"rate must be >= 0, got {rate}")
    return round(price * (1 + rate), 2)


def merge_carts(cart_a: dict, cart_b: dict) -> dict:
    """
    Merge two {sku: qty} carts, summing quantities for shared SKUs.
    """
    merged = dict(cart_a)
    for sku, qty in cart_b.items():
        merged[sku] = merged.get(sku, 0) + qty
    return merged


# ──────────────────────────────────────────────────────────────
# TASK 1 — Why `src/` layout forces an install (hands-on + write-up)
# ──────────────────────────────────────────────────────────────
# In your scratch dir, build a MINIMAL src-layout package:
#
#   scratch/
#   ├── pyproject.toml          # minimal: name + version (see hint below)
#   ├── src/
#   │   └── shop/
#   │       ├── __init__.py
#   │       └── pricing.py      # put a function apply_tax(price, rate) here
#   └── tests/
#       └── test_pricing.py     # `from shop.pricing import apply_tax`
#
#   Hint for a minimal pyproject.toml:
#       [project]
#       name = "shop"
#       version = "0.0.1"
#       [build-system]
#       requires = ["setuptools"]
#       build-backend = "setuptools.build_meta"
#
# STEP A: from scratch/, run `pytest -q`. It should FAIL to import
#         `shop` (ModuleNotFoundError). Observe that.
# STEP B: run `pip install -e .` from scratch/, then `pytest -q`
#         again. It should now PASS.
#
# Then, in THIS file:
#   1. Write a comment explaining WHY step A failed even though the
#      code was clearly right there in src/shop/pricing.py.
#   2. Write test_apply_tax_adds_eighteen_percent that asserts
#      apply_tax(100.0, 0.18) == 118.0   (uses the local copy above)

# YOUR ANSWER HERE (as a comment)
# WHY DID STEP A FAIL? ...

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 2 — Reproduce the `import file mismatch` error
# ──────────────────────────────────────────────────────────────
# In your scratch dir's tests/, create TWO files that share a
# basename but live in different subfolders, with NO __init__.py:
#
#   tests/api/test_utils.py  ->  def test_api(): assert True
#   tests/db/test_utils.py   ->  def test_db():  assert True
#
# Run `pytest -q` (default prepend mode) and watch it break during
# COLLECTION (not during a test).
#
# In THIS file:
#   1. Paste the ONE-LINE headline of the error you saw, as a comment.
#   2. In a comment, explain in your own words WHY two files named
#      test_utils.py collide under the default import mode.
#   3. Write test_merge_carts_sums_shared_skus asserting:
#         merge_carts({"A": 1, "B": 2}, {"B": 3, "C": 1})
#             == {"A": 1, "B": 5, "C": 1}

# YOUR ANSWER HERE (as comments)
# ERROR HEADLINE: ...
# WHY THEY COLLIDE: ...

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 3 — Fix it TWO ways, then choose (hands-on + decision)
# ──────────────────────────────────────────────────────────────
# Using the SAME broken scratch/tests/ from Task 2:
#
#   FIX A: add empty __init__.py to tests/, tests/api/, tests/db/,
#          then run `pytest -q`. Confirm it PASSES.
#   FIX B: delete those __init__.py again, then run
#          `pytest -q --import-mode=importlib`. Confirm it PASSES too.
#
# In THIS file:
#   1. In a comment, state which fix you'd choose for a BRAND-NEW
#      project today, and give ONE concrete reason.
#   2. In a comment, name the THIRD possible fix that needs no config
#      change at all (hint: it's about how you NAME files).
#   3. Write test_apply_tax_negative_rate_raises asserting that
#      apply_tax(100.0, -0.1) raises ValueError.

# YOUR ANSWER HERE (as comments)
# CHOSEN FIX + REASON: ...
# THIRD FIX (no config): ...

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# TASK 4 — conftest placement as an organizing decision
# ──────────────────────────────────────────────────────────────
# You have a fixture `fake_clock` that only INTEGRATION tests should
# see, and a fixture `sample_cart` that EVERY test should see.
#
# In a comment below, state the exact file path (relative to the repo
# root, assuming a tests/unit/ and tests/integration/ split) where
# you would place EACH fixture so that scope is correct — and say in
# one line what goes wrong if you instead dump both into a single
# top-level tests/conftest.py.
#
# Then, to prove you can consume a fixture by NAME (no import), write:
#   - a fixture `sample_cart` in THIS file returning {"A": 2, "B": 1}
#   - test_sample_cart_total_qty that takes `sample_cart` as an
#     argument and asserts the total quantity across all SKUs == 3

# YOUR ANSWER HERE (as comments)
# fake_clock goes in:  ...
# sample_cart goes in: ...
# WHAT BREAKS if both go in one top-level conftest.py: ...

# YOUR CODE HERE


# ──────────────────────────────────────────────────────────────
# BONUS — The "green locally, broken on install" trap
# ──────────────────────────────────────────────────────────────
# A teammate on a FLAT layout (package at repo root, no src/) ships a
# release. Tests were all green in CI, but users who `pip install` the
# package get `ModuleNotFoundError: No module named 'shop.discounts'`.
# The discounts.py file exists in the repo and imports fine locally.
#
# As comments below, answer:
#   1. How can the tests be green while the installed package is broken?
#      (What is the flat layout letting the test suite import?)
#   2. What SINGLE layout change would have caught this before release,
#      and WHY does it catch it?
#   3. Write the two-command CI sequence (as a comment) that guarantees
#      the suite tests the BUILT package rather than the source tree.

# YOUR ANSWER HERE (as comments)
# 1. ...
# 2. ...
# 3. ...