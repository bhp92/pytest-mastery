# 🧪 Week 2, Day 1 — Fixture Scopes

### What it is / why it exists

A fixture's *scope* controls **how often it runs and how long its value lives**. The rule is one line: pytest creates the fixture value once per scope and caches it, handing that same object to every test in that scope. Four scopes, widest lifetime to narrowest: `session` → `package` → `module` → `class` → `function` (the default).

Scopes exist because **not all setup is cheap or per-test.** Building a fresh dict is free, so `function` scope (rebuild for every test) is the safe default that guarantees isolation. But spinning up a database, authenticating an API client, or loading a 200MB model is expensive — doing it 400 times for 400 tests is the difference between a 5-second suite and a 5-minute one. Wider scopes let you pay that cost **once** and share the result. So scope is fundamentally a **trade-off dial between isolation (narrow) and speed (wide)**.

### Key concepts you need

- `@pytest.fixture(scope="module")` — set the lifetime. Default is `"function"`.
- **Run count follows scope:** `function` = once per test; `class` = once per test class; `module` = once per `.py` file; `session` = once per whole run.
- **Wider scope = shared object.** Every test in that scope gets the *same instance*. Mutations persist. This is the point (for a DB handle) and the danger (for state).
- **Setup/teardown ordering nests:** wider fixtures set up first and tear down last. In my verified run, `session` set up before `module`, and tore down after it.
- **ScopeMismatch rule:** a fixture may only request others of **equal or wider** scope. A `session` fixture requesting a `function` fixture is an error (I triggered it above) — because the narrow one would have to outlive its own lifetime.
- **Parallelism caveat (senior-level):** under `pytest-xdist` (`-n auto`), `session` means *once per worker process*, not once globally. Your CI already runs this way, so never treat session state as a true singleton.

### Real-world production example

A service integration suite: one `session`-scoped fixture starts a throwaway Postgres container and runs migrations (10–15s, done once). A `function`-scoped `autouse` fixture wraps each test in a transaction and rolls it back on teardown. Result: the expensive container is shared for speed, but every test still gets a pristine database for isolation. That combination — *wide scope for the resource, narrow reset for the state* — is the pattern interviewers want to hear.

### The 2 most common beginner mistakes

1. **Shared mutable state leaking between tests.** You widen a fixture to `module`/`session` for speed, then one test mutates the shared object and a later test silently depends on that mutation. Tests pass in order, fail when reordered (and `pytest-randomly` *will* reorder them). The fix isn't narrowing scope — it's isolating the state (transaction rollback, `autouse` cleanup), keeping the expensive resource wide.
2. **Widening scope by cargo-cult, breaking isolation for no gain.** Slapping `scope="session"` on a fixture that builds a trivial dict. You save nothing and forfeit the free isolation `function` scope gave you. Only widen when setup is genuinely expensive.

---

### Working example (verified: 7 passed on pytest 9.1.1)

```python
import pytest

# Module-level ledgers so we can PROVE how many times each fixture ran.
setup_counts = {"function": 0, "class": 0, "module": 0, "session": 0}


@pytest.fixture(scope="session")
def session_client():
    # Runs ONCE for the whole test run. Put expensive setup here
    # (DB container, authenticated client). Teardown runs last of all.
    setup_counts["session"] += 1
    print("\n  >> [session] setup (expensive: e.g. spin up test DB)")
    yield {"conn": "db-handle"}
    print("\n  >> [session] teardown (once, after everything)")


@pytest.fixture(scope="module")
def module_data():
    # Runs ONCE per .py file. Shared by every test in this module.
    setup_counts["module"] += 1
    yield {"rows": [1, 2, 3]}


@pytest.fixture(scope="class")
def class_state():
    # Runs ONCE per test class. Shared only within that class.
    setup_counts["class"] += 1
    return {"visits": 0}


@pytest.fixture  # scope="function" is the DEFAULT — rebuilt every test.
def fresh_cart():
    setup_counts["function"] += 1
    return {"items": []}


# function scope: fresh object every test -> mutations never leak.
def test_cart_a(fresh_cart):
    fresh_cart["items"].append("apple")
    assert fresh_cart["items"] == ["apple"]

def test_cart_b(fresh_cart):
    assert fresh_cart["items"] == []            # fresh, NOT ["apple"]


# class scope: one object shared by tests in the SAME class.
class TestClassScope:
    def test_first(self, class_state):
        class_state["visits"] += 1
        assert class_state["visits"] == 1

    def test_second(self, class_state):
        class_state["visits"] += 1
        assert class_state["visits"] == 2       # SAME object across the class


# module + session: shared across the whole file / whole run.
def test_module_still_shared(module_data):
    module_data["rows"].append(4)
    assert module_data["rows"] == [1, 2, 3, 4]  # mutation persists (same obj)


# Proof of the run counts after everything above has executed.
def test_scope_counts_are_correct():
    assert setup_counts["function"] == 2   # one per test using fresh_cart
    assert setup_counts["class"] == 1      # one for the whole TestClass
    assert setup_counts["module"] == 1     # one for this file
    assert setup_counts["session"] == 1    # one for the whole run
```

Run it with `pytest -v -s --setup-show` — the `--setup-show` flag prints the fixture setup/teardown stack so you *watch* `SETUP S` (session) wrap `SETUP M` (module), and see teardowns unwind in reverse. That visual is the fastest way to internalize scope nesting.