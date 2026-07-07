# 🧪 Week 1, Day 1 — Install & First Test

### What is pytest and why does it exist?

Python ships with `unittest`, which works but is verbose — you inherit from classes, call `self.assertEqual(...)`, and write a lot of boilerplate. pytest was built to fix that. It lets you write a plain function starting with `test_`, use a bare `assert` statement, and get rich, readable failure output automatically. No classes required, no inheritance, no ceremony.

At a senior level, the answer to *"why pytest over unittest?"* isn't just "it's simpler." It's: pytest has a vastly superior plugin ecosystem, fixture injection via function arguments (not `setUp`/`tearDown`), parametrize built-in, and first-class support for mocking, coverage, async, and CI — all things you'll use in production.

---

### Key concepts for Day 1

**Test discovery** — pytest finds tests automatically. It looks for files matching `test_*.py` or `*_test.py`, then inside those files for functions starting with `test_`. You never have to register a test or add it to a suite.

**The `assert` statement** — pytest rewrites Python's `assert` at collection time using AST introspection. When an assertion fails, it shows you the actual values on both sides. This is not magic — it's bytecode rewriting, and it only works inside test files collected by pytest.

**Exit codes** — pytest returns `0` (all passed), `1` (some failed), `2` (interrupted), `5` (no tests collected). In CI pipelines, these codes are what triggers a failed build — something a senior engineer must understand.

**`pytest.ini` / `pyproject.toml`** — your repo already has a `pytest.ini`. This is where you configure the test root, markers, output format, and more. Senior engineers always have this file — it stops the "works on my machine" problem.

---

### One real-world production example

At a payments company, a new engineer writes:

```python
def test_charge_amount():
    result = process_charge(100)
    assert result == True       # Will pass for result = 1 also as bool is subclass of int. True == 1 -> True & False == 0 -> Ture
```

This passes. But `process_charge` returns `1` (an integer), not `True`. In Python, `1 == True` is `True`. The test is lying. A senior engineer writes:

```python
assert result is True          # catches int/bool distinction, Also : Is this object the singleton boolean True
# or better:
assert isinstance(result, bool) and result # if type(result) == bool and result == Ture -> pass
```

This is Day 1 thinking: `assert` is powerful, but you must be precise about *what* you're asserting.

---

### The 2 most common beginner mistakes

**Mistake 1 — Naming a file `tests.py` instead of `test_tests.py` or putting it in a `tests/` folder without `__init__.py` issues.** pytest discovery follows specific rules. If your file isn't named `test_*.py`, pytest silently skips it. No error, no warning — just 0 tests collected. Beginners spend an hour confused why their tests "don't run."

**Mistake 2 — Writing `assert result == True` instead of `assert result`.** Asserting against the literal `True` introduces the `1 == True` trap above. The idiomatic pytest way is just `assert result` for truthy checks, or `assert result is True` when the boolean type specifically matters.

---