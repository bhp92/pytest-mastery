"""
============================================================================
Week 2 — Day 2 — Fixture Scopes
============================================================================

HOW TO RUN
----------
Place this file at:  exercises/week2_day2.py

Run just this file (verbose):
    pytest exercises/week2_day2.py -v

Run and SEE fixture setup/teardown output (print statements):
    pytest exercises/week2_day2.py -v -s

WATCH the scope nesting (the single best debugging flag for today):
    pytest exercises/week2_day2.py --setup-show

Confirm order-independence (Task 4 is designed to expose leaks):
    pytest exercises/week2_day2.py -p randomly -v      # if pytest-randomly installed

SCOPE FOR TODAY
---------------
Only Day 2 concepts:
  - scope= on @pytest.fixture: "function" (default), "class", "module", "session"
  - how many times a fixture runs at each scope
  - wider scope = ONE shared object handed to every test in that scope
  - the shared-mutable-state trap, and why it's a scope problem
  - the ScopeMismatch rule (wide fixtures may not request narrow ones)

Keep it to scope. You do NOT need conftest.py yet (that's Day 3) and you do
NOT need deep yield-teardown patterns (that's Day 4). A module-level counter
dict is enough to PROVE how often each fixture ran.

Complete the tasks IN ORDER. Each builds on the previous one.
Write ONLY your own code. No solutions are provided.
============================================================================
"""

import pytest


# A shared ledger you will use across several tasks to PROVE run counts.
# (It lives at module level on purpose — it is NOT a fixture.)
setup_counts = {"function": 0, "class": 0, "module": 0, "session": 0}


# ---------------------------------------------------------------------------
# TASK 1 — Prove the default (function) scope isolates tests
# ---------------------------------------------------------------------------
# a) Define a fixture `fresh_cart` (default scope — do NOT pass scope=) that
#    increments setup_counts["function"] and returns {"items": []}.
# b) Write `test_cart_add` that requests fresh_cart, appends "apple" to
#    items, and asserts items == ["apple"].
# c) Write `test_cart_is_isolated` that requests fresh_cart and asserts
#    items == []  (i.e. the "apple" from the other test did NOT leak).
#
# Goal: prove function scope rebuilds the object per test -> free isolation.

@pytest.fixture
def fresh_cart():
    setup_counts["function"] += 1
    return {"items": []}

def test_cart_add(fresh_cart):
    fresh_cart["items"].append("apple")
    assert fresh_cart["items"] == ["apple"]

def test_cart_is_isolated(fresh_cart):
    assert fresh_cart["items"] == []

# ---------------------------------------------------------------------------
# TASK 2 — class scope: one object shared WITHIN a class
# ---------------------------------------------------------------------------
# a) Define a fixture `class_state` with scope="class" that increments
#    setup_counts["class"] and returns {"visits": 0}.
# b) Write a test class `TestVisits` with two methods, each taking
#    `self` and `class_state`:
#       - test_first  : visits += 1, assert visits == 1
#       - test_second : visits += 1, assert visits == 2   (SAME object)
#
# Goal: prove class scope shares ONE instance across the class's tests,
#       and contrast that with Task 1's per-test freshness.

@pytest.fixture(scope="class")
def class_state():
    setup_counts["class"] += 1
    return {"visits": 0}

class TestVisits:
    def test_first(self, class_state):
        class_state["visits"] += 1
        assert class_state["visits"] == 1

    def test_second(self, class_state):
        class_state["visits"] += 1
        assert class_state["visits"] == 2

# ---------------------------------------------------------------------------
# TASK 3 — module scope: built once for the whole file
# ---------------------------------------------------------------------------
# a) Define a fixture `module_registry` with scope="module" that increments
#    setup_counts["module"] and returns {"loaded": True, "rows": [1, 2, 3]}.
# b) Write two plain tests, `test_registry_a` and `test_registry_b`, that
#    each request module_registry and assert loaded is True.
# c) Add a THIRD test `test_module_built_once` that asserts
#    setup_counts["module"] == 1   (it ran once no matter how many tests used it).
#
# Goal: prove module scope runs a single time per file and is cached.

@pytest.fixture(scope="module")
def module_registry():
    setup_counts["module"] += 1
    return {"loaded": True, "rows": [1, 2, 3]}

def test_registry_a(module_registry):
    assert module_registry["loaded"] is True

def test_registry_b(module_registry):
    assert module_registry["loaded"] is True

def test_registry_c(module_registry):
    assert setup_counts["module"] == 1

# ---------------------------------------------------------------------------
# TASK 4 — session scope + the shared-mutable-state TRAP
# ---------------------------------------------------------------------------
# This is the core interview trap. Read carefully.
#
# a) Define a fixture `session_store` with scope="session" that increments
#    setup_counts["session"] and returns {"writes": []}  (a mutable list).
# b) Write `test_write_one` that requests session_store, appends "a" to
#    writes, and asserts writes == ["a"].
# c) Write `test_write_two` that requests session_store, appends "b", and
#    asserts writes == ["a", "b"].
#       -> Notice you had to encode the leak into the assertion. The mutation
#          from test_write_one PERSISTED because both tests share one object.
# d) In a comment, answer: this test pair passes in file order. Why is it
#    still a bug? What breaks it, and what is the RIGHT fix (keep the scope
#    wide for the resource, isolate the state some other way)?

# Answer: pytest-randomly could execute the tests in any order. `assert session_store["writes"] == ["a", "b"]` could fail if test_write_two is executed first. Do not know the fix.

#
# Goal: feel why wide scope + mutable state = order-dependent tests, and
#       articulate the production fix (reset/rollback per test, not narrowing).

@pytest.fixture(scope="session")
def session_store():
    setup_counts["session"] += 1
    return {"writes": []}

def test_write_one(session_store):
    session_store["writes"].append("a")
    assert session_store["writes"] == ["a"]

def test_write_two(session_store):
    session_store["writes"].append("b")
    assert session_store["writes"] == ["a", "b"]

# ---------------------------------------------------------------------------
# BONUS — ScopeMismatch: what pytest forbids and why
# ---------------------------------------------------------------------------
# a) Define a function-scoped fixture `token` that returns "abc123".
# b) Define a fixture `authed_client` with scope="session" that requests
#    `token` as a parameter and returns {"auth": token}.
# c) Write `test_scope_mismatch` that requests authed_client.
#       -> Run it. It will ERROR (not fail) with ScopeMismatch. Read the
#          message; it names both scopes.
# d) Now FIX it so the test passes, and in a comment state the rule in one
#    line: which direction of dependency is legal (wide->narrow or
#    narrow->wide?) and the reason (a shared object cannot depend on one
#    that is rebuilt more often than itself).
#
# Goal: know the dependency-direction rule cold — a classic senior probe.
# ---------------------------------------------------------------------------

#@pytest.fixture
#def token():
#    return "abc123"
#
#@pytest.fixture(scope="session")
#def authed_client(token):
#    return {"auth": token}
#
#def test_scope_mismatch(authed_client):
#    assert authed_client["auth"] == "abc123"

# Why it's a bug even though it passes in file order. The two tests are coupled. test_write_two only passes because test_write_one ran first and left "a" behind in the shared session object 
# — so its assertion == ["a", "b"] is quietly asserting another test's side effect, not its own. A test should pass or fail on its own behavior alone.

# What breaks it. Anything that changes execution order or membership: pytest-randomly reordering the suite; running just pytest -k test_write_two; pytest-xdist (-n auto), 
# where session scope is per worker process so test_write_two may land on a worker that never ran test_write_one; or simply skipping/deleting test_write_one. 
# Your CI already runs xdist, so this isn't hypothetical.

# The right fix — decouple the resource from the state. Don't narrow the scope (that throws away the speed win). Keep the expensive resource session-scoped, 
# and reset the mutable state per test with a function-scoped autouse fixture:
# fix:

@pytest.fixture(scope="session")
def session_store():          # resource: built once
    return {"writes": []}

@pytest.fixture(autouse=True) # state: cleaned before every test
def _reset_store(session_store):
    session_store["writes"].clear()
    yield

def test_write_one(session_store):
    session_store["writes"].append("a")
    assert session_store["writes"] == ["a"]

def test_write_two(session_store):
    session_store["writes"].append("b")
    assert session_store["writes"] == ["b"]   # asserts only its own effect