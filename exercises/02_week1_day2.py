"""
WEEK 1 — DAY 2: Test Discovery Rules
=====================================
RUN INSTRUCTIONS:
1. Place this file at exercises/week1_day1.py in your pytest-mastery checkout.
2. As you complete each task, verify with:
       pytest --collect-only exercises/week1_day1.py -v
3. Once you THINK everything is fixed, run it for real:
       pytest exercises/week1_day1.py -v
4. Do the tasks in order — Task 3 depends on Task 2 being fixed first.
5. No solutions here. Comments only. Predict before you verify.
"""

# ─────────────────────────────────────────────
# TASK 1 — Fix the silent skip
# ─────────────────────────────────────────────
# This function is MEANT to be a real test, but pytest will not collect it
# as written. Before touching anything, write a one-line comment below
# predicting WHY it won't be collected. Then fix the name (not the body)
# so pytest discovers and runs it.

# Prediction: It won't be collected as the test name does not follow the naming convention required for pytest to collect it as test, test must begin with "test_"

#def check_addition():                           # fix: test_check_addition()
def test_check_addition():
    assert 2 + 2 == 4


# ─────────────────────────────────────────────
# TASK 2 — Fix the false positive
# ─────────────────────────────────────────────
# The function below WILL be collected by pytest as a test — but it isn't
# one. It's a helper meant to be called BY tests, not run as one (it takes
# an argument, which should already feel wrong for a test function).
# Rename/restructure it so pytest does NOT collect it, while keeping it
# usable as a helper in Task 3.

#def test_double(n):                             # fix: double(n)
def double(n):
    return n * 2


# ─────────────────────────────────────────────
# TASK 3 — Fix the broken test class
# ─────────────────────────────────────────────
# This class is meant to hold two passing tests. As written, pytest will
# skip the ENTIRE class with a collection warning. Identify the rule it
# violates and fix the class structure (not the test logic) so both
# methods below are collected. Then replace the placeholder assertion in
# test_doubling with a real one that uses your fixed Task 2 helper.

class TestMath:
    value = 10
#    def __init__(self):                         # I know for the test to be collected, we need to be remove the constructor
#        self.value = 10                         # declare without constructor, value = 10

#    def test_doubling(self):                    # fix: test_doubling(double(val))
    def test_doubling(self):
#        assert True  # replace with a real assertion using the Task 2 helper
        assert double(self.value) == 20

    def test_subtraction(self):                 # fix: test_subsraction()
        assert 10 - 4 == 6


# ─────────────────────────────────────────────
# TASK 4 — Predict, then prove it
# ─────────────────────────────────────────────
# Without running anything yet, write your prediction below for how many
# tests pytest will collect from this file once Tasks 1-3 are correctly
# fixed. Then run --collect-only and compare.

# Your prediction (count): 3
# Actual result (count): 3
# Explanation if they don't match:


# ─────────────────────────────────────────────
# BONUS — Scope it down
# ─────────────────────────────────────────────
# Without renaming anything above, figure out the pytest.ini (or
# pyproject.toml [tool.pytest.ini_options]) setting that would make pytest
# discover functions starting with "check_" instead of the default
# "test_" prefix. Write the exact config lines as a comment below — don't
# apply it, just prove you know the option name and syntax.

# Config lines:
#
# pytest.in
# [pytest]
# python_functions = check_*
#
# pyproject.toml
# [tool.pytest.ini_options]
# python_functions = ["check_*"]