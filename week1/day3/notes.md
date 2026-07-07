# 🧪 Week 1, Day 3 — Assertions Deep Dive

### What it is and why it exists

Every other testing framework (unittest, JUnit, etc.) forces you to memorize a zoo of methods: `assertEqual`, `assertIn`, `assertIsInstance`, `assertRaises`... pytest's bet was: *just use Python's native `assert`.* To make that viable, pytest hooks into import machinery and **rewrites the AST of every `assert` statement** in files it collects. When `assert x == y` fails, pytest doesn't just say "AssertionError" — it walks the expression tree and shows you the actual values of `x` and `y`, and for collections, a structured diff (added/removed items, dict key differences, etc.).

This only happens in files pytest imports through its own import hook — that's why plain `python your_test.py` won't give you the rich diffs, but `pytest your_test.py` will.

---

### Key concepts for Day 3

1. **Assertion rewriting** — pytest parses the test module's AST and injects introspection code around `assert`. This is why `assert some_dict == expected_dict` gives you a readable diff instead of just `AssertionError`.
2. **`pytest.raises(ExceptionType, match=r"regex")`** — a context manager that:
   - Fails the test if the block does *not* raise `ExceptionType`
   - If `match` is given, runs `re.search(pattern, str(exception))` — **not** `re.match`, despite the name. It searches anywhere in the string.
   - Returns an `ExceptionInfo` object you can inspect after the block: `exc_info.value`, `exc_info.type`, `exc_info.traceback`.
3. **`pytest.warns(WarningType)`** — same idea but for `warnings.warn(...)` calls. Used heavily when deprecating APIs: you want to *prove* the warning fires without breaking the calling code.
4. **Multiple assertions per test** — pytest doesn't stop at the first failing test in a file, but it *does* stop at the first failing `assert` inside one test function (unless you use `pytest.check` / soft-assert plugins, which is a Week 5+ topic).

---

### One real-world production example

Say you're deprecating a `get_user(id)` function in favor of `get_user_by_id(id)` during a migration sprint. You keep the old function working but make it emit a warning:

```python
def get_user(id):
    warnings.warn("get_user is deprecated, use get_user_by_id", DeprecationWarning)
    return get_user_by_id(id)
```

In CI, you test this with `pytest.warns(DeprecationWarning, match="get_user_by_id")` — proving the warning exists *and* mentions the replacement, so if someone "cleans up" the code and silently drops the warning, the test suite catches it before it ships.

---

### The 2 most common beginner mistakes

1. **Treating `match` like `re.match` (anchored at the start).** People write `match=r"negative"` expecting it to require the string to *start* with "negative," get confused when it "over-matches," or forget to escape regex metacharacters like `$`, `(`, `)`, `.` that show up naturally in error messages (e.g. `"Price cannot be $-10"` — that unescaped `$` and `-` can silently change what the regex actually checks).
2. **Putting too much or too little code inside the `with pytest.raises(...):` block.** Too little (a mistake you can make going forward): if you put an assert after the raising call inside the block, that assert never executes — the exception already unwound the block — but the test still "passes," giving false confidence in something you never actually checked. Too much: wrapping several calls in one block so an *earlier* line raises the same exception type for the *wrong* reason, and the test passes without ever exercising the line you meant to test.

---