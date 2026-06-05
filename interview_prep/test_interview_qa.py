"""
Interview Prep — 12 Senior-Level Pytest Questions
Each question is followed by a demonstration that proves you know the answer.

Run with: pytest interview_prep/test_interview_qa.py -v
"""
import pytest
import sqlite3
import sys


# ══════════════════════════════════════════════════════════════════════════════
# Q1: Difference between function-scope and session-scope fixtures
# ══════════════════════════════════════════════════════════════════════════════

counter_calls = {"function": 0, "session": 0}


@pytest.fixture(scope="function")
def function_scoped():
    counter_calls["function"] += 1
    return counter_calls["function"]


@pytest.fixture(scope="session")
def session_scoped():
    counter_calls["session"] += 1
    return counter_calls["session"]


def test_scope_q1_a(function_scoped, session_scoped):
    assert function_scoped == 1   # fresh each test
    assert session_scoped == 1    # created once


def test_scope_q1_b(function_scoped, session_scoped):
    assert function_scoped == 2   # new instance!
    assert session_scoped == 1    # same instance


# ══════════════════════════════════════════════════════════════════════════════
# Q2: How fixture injection works — conftest.py sharing
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def base_config():
    return {"timeout": 30, "retries": 3, "env": "test"}


def test_fixture_injection(base_config):
    """pytest matched the param name 'base_config' to the fixture above."""
    assert base_config["env"] == "test"


# ══════════════════════════════════════════════════════════════════════════════
# Q3: monkeypatch vs unittest.mock.patch
# ══════════════════════════════════════════════════════════════════════════════

import os

def get_db_url():
    return os.environ.get("DATABASE_URL", "sqlite:///default.db")


def test_monkeypatch_env(monkeypatch):
    """monkeypatch: no decorator, auto-restore, pytest-native."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://test/db")
    assert get_db_url() == "postgresql://test/db"
    # After test: DATABASE_URL is automatically restored


def test_mocker_patch_env(mocker):
    """mocker.patch: full MagicMock power, auto-cleanup via pytest-mock."""
    mocker.patch.dict(os.environ, {"DATABASE_URL": "mysql://test/db"})
    assert get_db_url() == "mysql://test/db"


# ══════════════════════════════════════════════════════════════════════════════
# Q4: Sharing fixtures via conftest.py
# ══════════════════════════════════════════════════════════════════════════════

# Demonstrate with a local fixture — in real code this would be in conftest.py
@pytest.fixture
def shared_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE products (id INT, name TEXT, price REAL)")
    yield conn
    conn.close()


def test_shared_db_insert(shared_db):
    shared_db.execute("INSERT INTO products VALUES (1, 'Widget', 9.99)")
    row = shared_db.execute("SELECT name FROM products").fetchone()
    assert row[0] == "Widget"


# ══════════════════════════════════════════════════════════════════════════════
# Q5: xfail and strict=True
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.xfail(reason="Bug #101: edge case in parser — PR in review")
def test_xfail_expected():
    assert int("not-a-number") == 0  # will raise ValueError → xfailed ✓


@pytest.mark.xfail(strict=False)
def test_xfail_passes_unexpectedly():
    assert 1 == 1  # passes → "xpassed" warning (not a failure with strict=False)


# ══════════════════════════════════════════════════════════════════════════════
# Q6: Parallel testing with pytest-xdist
# ══════════════════════════════════════════════════════════════════════════════
# Not demonstrable in a single file, but here's the pattern:
#
#   pytest -n auto                  # auto-detect CPU count
#   pytest -n 4                     # 4 workers
#   pytest -n auto --dist=loadfile  # keep test file on same worker
#
# Key gotcha: session-scoped fixtures are NOT shared across workers.
# Each worker creates its own session. Design for this.

def test_xdist_note():
    """Marker to remind you about xdist gotchas."""
    assert True  # placeholder — run: pytest -n auto to verify parallelism


# ══════════════════════════════════════════════════════════════════════════════
# Q7: Indirect parametrize
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def authenticated_user(request):
    """Receives role via request.param when called indirectly."""
    role = request.param
    return {
        "role":  role,
        "token": f"token-for-{role}",
        "perms": {
            "admin":  ["read", "write", "delete", "admin"],
            "editor": ["read", "write"],
            "viewer": ["read"],
        }[role],
    }


@pytest.mark.parametrize("authenticated_user, action, allowed", [
    ("admin",  "delete", True),
    ("editor", "write",  True),
    ("editor", "delete", False),
    ("viewer", "read",   True),
    ("viewer", "write",  False),
], indirect=["authenticated_user"])
def test_permissions(authenticated_user, action, allowed):
    has_permission = action in authenticated_user["perms"]
    assert has_permission == allowed


# ══════════════════════════════════════════════════════════════════════════════
# Q8: Custom plugin hooks (see week5/conftest.py for full example)
# ══════════════════════════════════════════════════════════════════════════════

# The key hooks to know:
#   pytest_addoption       → add --my-flag CLI option
#   pytest_collection_modifyitems → filter/reorder/skip collected tests
#   pytest_runtest_makereport    → inspect pass/fail after each test
#   pytest_configure       → global config at startup
#   pytest_sessionfinish   → cleanup after all tests

def test_hooks_knowledge():
    hooks = [
        "pytest_addoption",
        "pytest_collection_modifyitems",
        "pytest_runtest_makereport",
        "pytest_configure",
        "pytest_sessionfinish",
    ]
    assert len(hooks) == 5  # know all 5


# ══════════════════════════════════════════════════════════════════════════════
# Q9: pytest.raises with message matching
# ══════════════════════════════════════════════════════════════════════════════

class InsufficientFundsError(Exception):
    pass


def withdraw(balance: float, amount: float) -> float:
    if amount > balance:
        raise InsufficientFundsError(
            f"Cannot withdraw {amount:.2f}, balance is {balance:.2f}"
        )
    return balance - amount


def test_raises_with_match():
    with pytest.raises(InsufficientFundsError, match=r"Cannot withdraw 150\.00"):
        withdraw(100.0, 150.0)


def test_raises_captures_value():
    with pytest.raises(InsufficientFundsError) as exc_info:
        withdraw(50.0, 200.0)
    assert "200.00" in str(exc_info.value)
    assert exc_info.type is InsufficientFundsError


# ══════════════════════════════════════════════════════════════════════════════
# Q10: tmp_path vs tmpdir
# ══════════════════════════════════════════════════════════════════════════════

def test_tmp_path_is_pathlib(tmp_path):
    """tmp_path: modern pathlib.Path — RECOMMENDED."""
    from pathlib import Path
    assert isinstance(tmp_path, Path)
    config = tmp_path / "config.json"
    config.write_text('{"debug": true}')
    assert config.read_text() == '{"debug": true}'


def test_tmpdir_is_legacy(tmpdir):
    """tmpdir: legacy py.path.local — still works, but prefer tmp_path."""
    import py
    assert isinstance(tmpdir, py.path.local)


# ══════════════════════════════════════════════════════════════════════════════
# Q11: Testing CLI tools
# ══════════════════════════════════════════════════════════════════════════════

import argparse
import io
from contextlib import redirect_stdout


def cli_main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--greet", default="World")
    parsed = parser.parse_args(args)
    print(f"Hello, {parsed.greet}!")
    return 0


def test_cli_with_monkeypatch(monkeypatch, capsys):
    """Use capsys to capture stdout/stderr."""
    monkeypatch.setattr("sys.argv", ["prog", "--greet", "Pytest"])
    cli_main(["--greet", "Pytest"])
    captured = capsys.readouterr()
    assert "Hello, Pytest!" in captured.out


# ══════════════════════════════════════════════════════════════════════════════
# Q12: Debugging flaky tests
# ══════════════════════════════════════════════════════════════════════════════

# Strategy cheatsheet (not runnable — reference only):
#
# 1. Reproduce:    pytest --count=20 test_flaky.py          (pytest-repeat)
# 2. Order issues: pytest --randomly-seed=12345             (pytest-randomly)
# 3. Slow timing:  pytest --durations=10                    (find slow tests)
# 4. Debug live:   pytest --pdb test_flaky.py               (drop into pdb)
# 5. See output:   pytest -s test_flaky.py                  (no capture)
# 6. Isolate:      pytest test_flaky.py::test_specific -v   (single test)
#
# Root causes of flakiness:
#   - Shared mutable state in session/module fixtures
#   - Time-dependent assertions (use freezegun or mock datetime)
#   - Non-deterministic ordering (dicts pre-3.7, sets, threads)
#   - Port conflicts in integration tests (use dynamic ports)

def test_deterministic_example():
    """Always passes — demonstrates stable test design."""
    data = {"b": 2, "a": 1, "c": 3}
    assert sorted(data.keys()) == ["a", "b", "c"]  # sorted(), not dict order
