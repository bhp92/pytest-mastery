# Week 2 — Fixtures

**Goal:** Master pytest's core power feature — provide test dependencies cleanly, control their lifetime, and share them without imports.

---

## Day 1 — Fixture Basics (40 min)
- The `@pytest.fixture` decorator — a function that supplies data or state
- Use a fixture by naming it as a test parameter (no import needed)
- The `request` object and what pytest injects for you
- **Exercise:** `exercises/week2_day1.py`

## Day 2 — Fixture Scopes (40 min)
- `function` (default) / `class` / `module` / `session` — when each makes sense
- Expensive setup (DB connections, clients) belongs in a wider scope
- Scope bugs: shared mutable state leaking between tests
- **Exercise:** `exercises/week2_day2.py`

## Day 3 — conftest.py Patterns (40 min)
- Shared fixtures live in `conftest.py` — discovered automatically up the tree
- Discovery order: the most-local fixture wins when names clash
- Overriding a parent fixture in a child directory
- **Exercise:** `exercises/week2_day3.py`

## Day 4 — Yield Fixtures (40 min)
- Setup + teardown in one fixture using `yield`
- Everything after `yield` runs on teardown, even if the test fails
- Why `yield` beats `request.addfinalizer` for readability
- **Exercise:** `exercises/week2_day4.py`

## Day 5 — Fixture Params (40 min)
- `params=[...]` runs every dependent test once per value
- Read the value with `request.param`
- `indirect=True` and custom `ids=` for readable test names
- **Exercise:** `exercises/week2_day5.py`

---

## Run This Week's Tests
```bash
cd week2
pytest -v                    # annotated walkthrough in test_fixtures.py
```