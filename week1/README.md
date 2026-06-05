# Week 1 — Foundations

**Goal:** Write your first tests, understand how pytest finds and runs them, and learn assertions.

---

## Day 1 — Install & First Test (40 min)
- `pip install pytest`
- Create `test_hello.py`, write `def test_something(): assert 1 + 1 == 2`
- Run `pytest -v` — understand the output
- **Exercise:** `exercises/week1_day1.py`

## Day 2 — Test Discovery Rules (40 min)
- Files must be named `test_*.py` or `*_test.py`
- Functions must start with `test_`
- Classes must start with `Test` (no `__init__`)
- conftest.py — what it is and where it goes
- **Exercise:** `exercises/week1_day2.py`

## Day 3 — Assertions Deep Dive (40 min)
- pytest rewrites `assert` to show you *exactly* what failed
- `pytest.raises(ExceptionType, match=r"regex")`
- `pytest.warns(UserWarning)`
- **Exercise:** `exercises/week1_day3.py`

## Day 4 — Running Tests Selectively (40 min)
- `-k "keyword"` — run matching test names
- `-m marker` — run marked tests
- `-x` — stop on first failure
- `--tb=short|long|no` — control traceback verbosity
- `-s` — show print statements
- **Exercise:** `exercises/week1_day4.py`

## Day 5 — Organizing Test Files (40 min)
- Flat vs nested structure
- `src/` layout vs flat layout
- When to use `__init__.py`
- **Exercise:** `exercises/week1_day5.py`

---

## Run This Week's Tests
```bash
cd week1
pytest -v
```
