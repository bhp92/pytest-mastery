"""
Week 2: Fixtures
Run with: pytest week2/test_fixtures.py -v
"""
import pytest
import sqlite3


# ── Day 1: Basic fixture ───────────────────────────────────────────────────

@pytest.fixture
def sample_user():
    """A simple fixture returning a dict."""
    return {"id": 1, "name": "Alice", "role": "admin"}


def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"


def test_user_is_admin(sample_user):
    assert sample_user["role"] == "admin"


# ── Day 2: Fixture scopes ──────────────────────────────────────────────────

@pytest.fixture(scope="module")
def module_counter():
    """Created once per module. All tests in this file share it."""
    print("\n[module_counter] setup")
    counter = {"value": 0}
    yield counter
    print("\n[module_counter] teardown")


def test_counter_first(module_counter):
    module_counter["value"] += 1
    assert module_counter["value"] == 1


def test_counter_second(module_counter):
    module_counter["value"] += 1
    # NOTE: still 2 — same object, not reset between tests!
    assert module_counter["value"] == 2


# ── Day 3: conftest.py pattern (see conftest.py in this folder) ────────────

def test_uses_shared_db(db_connection):
    """db_connection comes from conftest.py — no import needed."""
    db_connection.execute("INSERT INTO users VALUES (99, 'Bob')")
    cursor = db_connection.execute("SELECT name FROM users WHERE id=99")
    assert cursor.fetchone()[0] == "Bob"


# ── Day 4: Yield fixture (setup + teardown) ────────────────────────────────

@pytest.fixture
def temp_file(tmp_path):
    """Creates a temp file, yields the path, then cleans up."""
    f = tmp_path / "data.txt"
    f.write_text("hello pytest")
    yield f
    # teardown: file is auto-cleaned by tmp_path, but we could do extra cleanup
    print(f"\n[temp_file] done with {f}")


def test_file_contents(temp_file):
    assert temp_file.read_text() == "hello pytest"


def test_file_exists(temp_file):
    assert temp_file.exists()


# ── Day 5: Fixture with params ─────────────────────────────────────────────

@pytest.fixture(params=["sqlite", "memory"], ids=["sqlite-file", "in-memory"])
def db_type(request, tmp_path):
    """Runs every test that uses this fixture twice — once per param."""
    if request.param == "sqlite":
        path = str(tmp_path / "test.db")
        conn = sqlite3.connect(path)
    else:
        conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INT, name TEXT)")
    yield conn
    conn.close()


def test_insert_item(db_type):
    """This test runs TWICE — once with sqlite file, once in-memory."""
    db_type.execute("INSERT INTO items VALUES (1, 'widget')")
    row = db_type.execute("SELECT name FROM items WHERE id=1").fetchone()
    assert row[0] == "widget"


# ── Fixture factory pattern (advanced) ────────────────────────────────────

@pytest.fixture
def make_user():
    """Factory fixture — tests call it to create customized users."""
    created = []

    def _make(name="Alice", role="viewer", active=True):
        user = {"name": name, "role": role, "active": active}
        created.append(user)
        return user

    yield _make
    # teardown: could clean up DB records here
    print(f"\n[make_user] cleaned up {len(created)} users")


def test_admin_user(make_user):
    admin = make_user(name="Bob", role="admin")
    assert admin["role"] == "admin"


def test_inactive_user(make_user):
    user = make_user(active=False)
    assert not user["active"]
