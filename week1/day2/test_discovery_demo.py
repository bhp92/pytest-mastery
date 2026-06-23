"""
Demonstrates pytest's discovery rules in one file.
Run: pytest --collect-only test_discovery_demo.py -v
"""

# ✅ COLLECTED — correct function prefix
def test_addition_is_correct():
    assert 1 + 1 == 2


# ❌ NOT COLLECTED — wrong prefix, looks like a test, isn't one.
# This is the "silent skip" trap. No error. No warning. Just... nothing.
def check_subtraction_is_correct():
    assert 5 - 3 == 2


# ❌ NOT COLLECTED as a test — helper function, no "test_" prefix on purpose.
# This is the CORRECT way to keep shared logic out of the test run.
def multiply(a, b):
    return a * b


# ✅ COLLECTED — uses the helper above, itself correctly prefixed
def test_multiply_helper():
    assert multiply(3, 4) == 12


# ✅ COLLECTED — class starts with "Test", no __init__, methods prefixed
class TestStringMethods:
    def test_upper(self):
        assert "abc".upper() == "ABC"

    def test_strip(self):
        assert "  abc  ".strip() == "abc"


# ❌ ENTIRE CLASS SKIPPED — has __init__, so pytest refuses to collect it,
# even though test_will_not_run looks perfectly valid.
class TestBroken:
    def __init__(self):
        self.x = 1

    def test_will_not_run(self):
        assert True