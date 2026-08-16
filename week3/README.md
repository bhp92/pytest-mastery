# Week 3 — Parametrize & Marks

**Goal:** Write DRY tests — cover many cases with one function — and use marks to select, skip, and label tests.

---

## Day 1 — @pytest.mark.parametrize (40 min)
- Single and multiple parameters in one decorator
- `argnames` as a `"a, b"` string vs a list, and the `argvalues` list of tuples
- One assertion, many cases — no copy-paste tests
- **Exercise:** `exercises/week3_day1.py`

## Day 2 — Nested Parametrize (40 min)
- Stacking decorators produces a Cartesian product of cases
- `pytest.param(...)` to attach per-case `marks=` and `id=`
- Marking a single case `xfail` without touching the others
- **Exercise:** `exercises/week3_day2.py`

## Day 3 — Built-in Marks (40 min)
- `skip` / `skipif` — conditional skipping (platform, version, env)
- `xfail` — expected failures, with `raises=` and `strict=`
- `filterwarnings` — treat or silence warnings per test
- **Exercise:** `exercises/week3_day3.py`

## Day 4 — Custom Marks (40 min)
- Register marks in `pytest.ini` (`unit`, `slow`, `integration`)
- Select with `-m unit` or exclude with `-m "not slow"`
- `--strict-markers` to catch typo'd mark names
- **Exercise:** `exercises/week3_day4.py`

## Day 5 — IDs & Mark Combos (40 min)
- Readable test IDs so failures point at the exact case
- Combining custom marks with `parametrize`
- Indirect parametrize: feed the value through a fixture
- **Exercise:** `exercises/week3_day5.py`

---

## Run This Week's Tests
```bash
cd week3
pytest -v                    # annotated walkthrough in test_parametrize.py
pytest -m "not slow"         # skip the slow-marked case
```