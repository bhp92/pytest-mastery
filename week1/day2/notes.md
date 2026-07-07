# 🧪 Week 1, Day 2 — Test Discovery Rules

### What it is and why it exists

**What it is:** Test discovery is pytest's algorithm for finding which files, classes, and functions to treat as tests — without you registering anything manually.

**Why it exists:** Convention over configuration. On a real codebase with hundreds of test files, nobody wants to maintain a master list of "tests to run." You follow naming rules, and `pytest` just finds everything.

---

### Key concepts for Day 2

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

    **Minimal example**

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

    **Realistic production-style example**

    ```python
    # tests/conftest.py
    import pytest
    import sqlite3
    from unittest.mock import MagicMock

    @pytest.fixture(scope="session")
    def db_connection():
        """One real connection for the whole test session. It is expenive to setup, so we don't wanto to recreate it for every single test."""
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE USERS (id INTEGERS, name TEXT)")
        yield conn                                                          # Hand connection to pytest/tests and pause fixture execution.
        conn.close()                                                        # Teardown: runs when pytest resumes/closes the generator.
    
    @pytest.fixture
    def db_session(db_connection):
        """Each test gets a clean transaction, rolled backer after, so tests don't leak state into each other even though they share one connection."""
        db_connection.execute("BEGIN")                                          # Start a transaction for this test.
        yield db_connection                                                     # Test executes with transaction open.
        db_connection.execute("ROLLBACK")                                       # Discard all changes made by the test.

    @pytest.fixture
    def mock_payment_gateway():
        gateway = MagicMock()
        gateway.charge.return_value = {"status": "success", "id": "txn_123"}
        return gateway

    def pytest_configure(config):
        """A hool (not a fixture) - runs once at startup, useful for registering custom markers so pytest doesn't warn about 'unknown marks'."""
        config.addinvalue_line("markers", "slow: marks tests as slow-running")
    ```

    ```python
    # tests/test_orers.py
    def test_create_user(db_session):
        db_session.execute("INSERT INTO users VALUES (1, 'Alice')")
        row = db_session.execute("SELECT name FROM users WHERE id=1").fetchone()
        assert row[0] == "Alice"

    def test_charge_customer(mock_payment_gateway):
        result = mock_payment_gateway.charge(amount=100)
        assert result["status"] == "success"
    ```

    Key things this shows:
        - fixture scoping (session vs default function)
        - fixtures depending on other fixtures (db_session uses db_connection)
        - mocking external services so tests stay fast and isolated,
        - a hook (pytest_configure) which is different mechanism from a fixture but lives in the same file.

    **Common mistakes**

    1. Putting conftest.py in the rong place, then importing it anyways. If someone writes from conftest import my_fixture in a test file, that's a sign they're fighting the tool. pytest fixtures are meant to be requested by name as a function argument, never imported.
    2. Oerusing broad scopes (session/module) for fixtures that mutate shared state. A session scoped database connection that isn't reset between tests can let one test's leftover data silently break another. Order dependent tests failures are often a conftest.py scoping bug in dsiguise.
    3. Putting everything in one giat root conftest.py. As project grows, people dump unrelated fixtures (Auth, db, API clients, mocks) into a single file instead of using nested conftest.py files per test subdirectory. This makes it hard to know which fixtures actually apply to which tests and slows everyone down huting through one huge file. 

- **rootdir & testpaths:** pytest determines a rootdir from `pytest.ini`/`pyproject.toml`/`setup.cfg` and your invocation args; `testpaths` can scope discovery
- **Custom discovery:** `python_files`, `python_classes`, `python_functions` ini options let you override the `test_` convention entirely
- **`--collect-only`:** shows exactly what would run, without running it — your best debugging tool for this topic

---

### One real-world production example

In a monorepo CI pipeline, `testpaths` is set in `pyproject.toml` to scope discovery away from `node_modules/`, vendored deps, and build artifacts (`norecursedirs` handles this too). Senior teams often add a CI step that runs `pytest --collect-only -q` and asserts the collected count doesn't unexpectedly drop — that catches a test silently going dark from a naming/import bug before it costs you a missed regression.

---

### The 2 most common beginner mistakes

1. **Silent skip** — writing `check_login()` instead of `test_login()`. No error, no warning — it just never runs. This is the dangerous one because it *looks* fine.
2. **The `__init__` trap** — putting a constructor on a `Test` class. Pytest emits a `PytestCollectionWarning` and skips the *entire class*, not just one method.

---