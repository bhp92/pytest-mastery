# Week 4 — Mocking & Patching

**Goal:** Isolate the unit under test — replace network, environment, and collaborators with fakes so tests are fast and deterministic.

---

## Day 1 — unittest.mock Basics (40 min)
- `Mock` / `MagicMock` — auto-spec'd stand-ins for any object
- `return_value` for fixed results, `side_effect` for sequences/exceptions
- Inspect calls with `call_count`, `call_args`, `call_args_list`
- **Exercise:** `exercises/week4_day1.py`

## Day 2 — pytest-mock (40 min)
- The `mocker` fixture — `mock.patch` with automatic teardown
- `mocker.patch` / `mocker.patch.object` for targeted replacement
- `mocker.spy` wraps the real callable but still records calls
- **Exercise:** `exercises/week4_day2.py`

## Day 3 — monkeypatch Fixture (40 min)
- `setattr` / `setitem` — swap attributes and dict entries, auto-restored
- `setenv` / `delenv` — control environment variables per test
- `chdir` / `syspath_prepend` for filesystem and import control
- **Exercise:** `exercises/week4_day3.py`

## Day 4 — Patching Strategies (40 min)
- Patch where the name is *used*, not where it's defined
- `patch` as a context manager for a narrow scope
- Mocking coroutines with `AsyncMock`
- **Exercise:** `exercises/week4_day4.py`

## Day 5 — Mocking Anti-Patterns (40 min)
- Over-mocking — tests that pass while the code is broken
- Asserting on implementation details instead of behavior
- When NOT to mock: prefer real objects for pure logic
- **Exercise:** `exercises/week4_day5.py`

---

## Run This Week's Tests
```bash
cd week4
pytest -v                    # annotated walkthrough in test_mocking.py
```