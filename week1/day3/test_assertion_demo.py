"""
DAY 3 - Assertion Deep Dive: working example
Run with pytest test_assertion_demo.py -v
"""

import re
import warnings
import pytest


# ── Code under test ─────────────────────────────────────────
def charge_card(amount: float) -> float:
    """Charge a card. Raises ValueError for invalid amounts."""
    if amount <= 0:
        raise ValueError(f"charge amount must be positive, got {amount}")
    return round(amount, 2)

def get_user(user_id: int) -> dict:
    """Deprecated: use get_user_by_id instead"""
    warnings.warn("get_user() is deprecated, use get_user_by_id() instead", DeprecationWarning, stacklevel=2)
    return get_user_by_id(user_id)

def get_user_by_id(user_id: int) -> dict:
    return {"id": user_id, "name": "Alice", "role": "admin"}


# ── 1. Plain assert — pytest rewrites this for a rich diff ──
def test_dict_equality_shows_diff():
    expected = {"id": 1, "name": "Alice", "role": "user"}
    actual = get_user_by_id(1)
    # Uncomment this line to SEE pytest's diff output — it will show
    # exactly which key differs (role: "admin" != "user"), not just
    # "AssertionError".
    # assert actual == expected
    assert actual["id"] == expected["id"]   # passes


# ── 2. pytest.raises — basic form ────────────────────────────
def test_negative_charge_raises():
    with pytest.raises(ValueError):
        charge_card(-18)


# ── 3. pytest.raises with match= (re.search, not re.match!) ──
def test_negative_charge_message():
    with pytest.raises(ValueError, match=r"must be positive"):
        charge_card(-18)
    # Gotcha: "-10" happens to be regex-safe here, but something like
    # "$-10" or "10.0)" would need re.escape() before matching.


# ── 4. Inspecting the exception after the block ──────────────
def test_negative_charge_exc_info():
    with pytest.raises(ValueError) as exc_info:
        charge_card(0)
    assert "0" in str(exc_info.value)
    assert exc_info.type is ValueError


# ── 5. pytest.warns — proving a deprecation warning fires ────
def test_user_emits_deprecation_warning():
    with pytest.warns(DeprecationWarning, match=r"get_user_by_id()"):
        result = get_user(1)
    assert result["name"] == "Alice"

# ── 6. Anti-pattern — too much code inside the raises block ──
def test_anti_pattern_too_much_in_block():
    # BAD (commented): if get_user_by_id ever raised ValueError for an
    # unrelated reason, this would still pass — for the wrong reason.
    # with pytest.raises(ValueError):
    #     get_user_by_id(1)      # doesn't raise
    #     charge_card(-10)       # this is what we meant to test
    # GOOD: isolate exactly the call under test
    with pytest.raises(ValueError):
        charge_card(-10)