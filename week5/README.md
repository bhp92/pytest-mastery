# Week 5 — Advanced Patterns

**Goal:** Reach for the right plugin without searching, measure coverage honestly, test async code, and extend pytest with your own hooks.

---

## Day 1 — Plugin Ecosystem (40 min)
- The plugins that matter: `pytest-cov`, `pytest-xdist`, `pytest-asyncio`
- Framework helpers: `pytest-django`, `pytest-httpx`
- How installed plugins register fixtures and options automatically
- **Exercise:** `exercises/week5_day1.py`

## Day 2 — Coverage Mastery (40 min)
- `--cov` for line coverage, `--cov-branch` for branch coverage
- Configure via `.coveragerc` (or `pyproject.toml`); `--cov-report=html`
- `--cov-fail-under=N` to gate CI on a coverage floor
- **Exercise:** `exercises/week5_day2.py`

## Day 3 — Async Testing (40 min)
- `pytest-asyncio` and `asyncio_mode = auto` (set in `pytest.ini`)
- Writing async tests and async fixtures
- Mocking coroutines with `AsyncMock` / `assert_awaited_once`
- **Exercise:** `exercises/week5_day3.py`

## Day 4 — Custom Plugin Hooks (40 min)
- `pytest_addoption` — add your own CLI flags (e.g. `--slow`)
- `pytest_collection_modifyitems` — filter, reorder, or skip collected tests
- `pytest_runtest_makereport` — inspect pass/fail per phase
- **Exercise:** `exercises/week5_day4.py`

## Day 5 — Fixture Factory Patterns (40 min)
- Factory fixtures — return a function tests call to build objects
- Track everything created and tear it all down at the end
- Chaining fixtures for complex, layered setups
- **Exercise:** `exercises/week5_day5.py`

---

## Run This Week's Tests
```bash
cd week5
pytest -v                                    # annotated walkthrough in test_advanced.py
pytest --slow                                # include the slow-marked test (see conftest.py)
pytest --cov=week5 --cov-branch --cov-report=term-missing
```