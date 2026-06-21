## STEP 1 — Test Discovery Rules

**What it is:** Test discovery is pytest's algorithm for finding which files, classes, and functions to treat as tests — without you registering anything manually.

**Why it exists:** Convention over configuration. On a real codebase with hundreds of test files, nobody wants to maintain a master list of "tests to run." You follow naming rules, and `pytest` just finds everything.

**Key concepts you need cold:**
- **Files:** `test_*.py` or `*_test.py`
- **Functions:** must start with `test_`
- **Classes:** must start with `Test`, must **not** define `__init__`, and their methods must start with `test_`
- **conftest.py:** never collected as a test itself, but discovered for fixtures/hooks — scope is the directory it lives in and below

    - Definition: conftest.py is a speacial pytest file that holds fixtures, hooks and configuration shared automatically across all test files in its directories and subdirectories. conftest.py do not require any import.
    - Why it exists: Without it, you'd face two problems.:
        1. Duplication: If five test files need a database connection, you'd wrute the setup code five times, or import it manually eveywhere.
        2. Implicit imports feel wrong: pytest wants you to just use a fixture by naming it as a test argument, not "from helpers import db_fixture" in every file. conftest.py is how pytest makes fixtures "ambient", visible to any testin scope without an import statement.

    It also solves a scoping problem: you can have multiple conftest.py files at different folder levels, and pytest merges them based on directory hierarchy. A fixture in tests/conftest.py is available everywhere under tests/; one in tests/api/conftest.py is only available under tests/api/.

    pytest auto-discovers fixtures defined there for every test file in scope. If you put @pytest.fixture def sample_number() inside test_basic.py itself, it'd work for tests in that same file too, but other test files would need an explicit import to use it. conftest.py is what makes it visible everywhere without an import.

    Minimal example

    ```python
    # tests/conftest.py
    import pytest

    @pytest.fixture
    def sample_number():
        return 42
    ```

    ```python
    # tests/test_basic.py
    def test_number_is_42(sample_number):
        assert sample_number == 42
    ```
    
    Notice: test_basic.py never imports anything from conftest.py. pytest discovers it automatically because of the filename and location.

- **rootdir & testpaths:** pytest determines a rootdir from `pytest.ini`/`pyproject.toml`/`setup.cfg` and your invocation args; `testpaths` can scope discovery
- **Custom discovery:** `python_files`, `python_classes`, `python_functions` ini options let you override the `test_` convention entirely
- **`--collect-only`:** shows exactly what would run, without running it — your best debugging tool for this topic

**Real-world example:** In a monorepo CI pipeline, `testpaths` is set in `pyproject.toml` to scope discovery away from `node_modules/`, vendored deps, and build artifacts (`norecursedirs` handles this too). Senior teams often add a CI step that runs `pytest --collect-only -q` and asserts the collected count doesn't unexpectedly drop — that catches a test silently going dark from a naming/import bug before it costs you a missed regression.

**Top 2 beginner mistakes:**
1. **Silent skip** — writing `check_login()` instead of `test_login()`. No error, no warning — it just never runs. This is the dangerous one because it *looks* fine.
2. **The `__init__` trap** — putting a constructor on a `Test` class. Pytest emits a `PytestCollectionWarning` and skips the *entire class*, not just one method.

## STEP 2 — Working ExampleThat's real output, not a guess — exactly 4 collected, `TestBroken` skipped with the exact warning I described above. This is the file you'll get from `pytest --collect-only`.

## STEP 3 — Your Exercise FileGo work through Tasks 1–4 and the bonus, then paste your solution here — I'll review it against what a senior engineer would actually write.