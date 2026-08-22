# 🧪 Week 2, Day 3 — conftest.py Patterns

### What it is / why it exists

A `conftest.py` is a special file pytest **discovers automatically** — you never import it. When pytest collects a test, it walks **up the directory tree** from that test file to the rootdir, and every `conftest.py` it passes along the way contributes its fixtures (and hooks, and plugins) to that test's scope. So a fixture defined in `conftest.py` is available, with no import, to every test at or below that directory.

It exists to solve the last problem plain fixtures leave open. On Day 1 you saw fixtures kill `setUp`/`tearDown` boilerplate; but a fixture written inside `test_orders.py` is only usable *in that file*. The moment two test files need the same `db` handle or `api_client`, your options without `conftest.py` are ugly: duplicate the fixture, or create a shared module and `import` it into every test file (which reintroduces exactly the import-coupling fixtures were meant to remove). `conftest.py` is pytest's answer: **share fixtures across files and directories with zero imports**, scoped by *location in the tree* rather than by import statements. That location-based, no-import sharing is the specific property senior interviewers probe.

### Key concepts you need

- **Auto-discovery, no import, ever.** Importing from `conftest.py` is an anti-pattern; pytest injects its fixtures by name. If you find yourself writing `from conftest import ...`, you've misunderstood the mechanism.
- **Discovery walks upward.** For a test at `week2/orders/test_x.py`, pytest collects `week2/orders/conftest.py`, then `week2/conftest.py`, then the root `conftest.py`. A fixture at any of those levels is in scope.
- **Most-local wins on name clash.** If both `week2/conftest.py` and `week2/orders/conftest.py` define `db`, tests inside `orders/` get the `orders/` one. This is *overriding a parent fixture in a child directory* — a deliberate, documented feature, not an accident.
- **Non-overridden names still resolve upward.** Overriding `db` in a child doesn't hide `base_url` — that still resolves at whatever level defines it.
- **`conftest.py` holds more than fixtures.** Hooks (`pytest_collection_modifyitems`), plugin registration, and `autouse` fixtures also live here. Your repo's `week2/conftest.py` already uses an `autouse` fixture (`clean_users_table`) that runs for every test in `week2/` without being requested.
- **A same-named override can request its parent.** A child `db(db)` that names `db` as its own parameter receives the *parent's* `db` (pytest resolves it to the next level up instead of recursing). This lets a child **extend** rather than **replace**. Verified on your pytest 9.1.1.

### Real-world production example

A service repo has a root `conftest.py` with a `session`-scoped fixture that spins up a throwaway Postgres container and an authenticated `api_client` — shared by the entire suite, no imports. Under `tests/billing/`, a child `conftest.py` overrides `api_client` with one carrying a billing-admin token, because only those tests need elevated scope. Every other directory keeps the root client. One fixture name, two behaviors, selected purely by *where the test lives*. That "override in a subtree for a local concern, inherit everything else" pattern is the everyday senior use of `conftest.py`.

### The 2 most common beginner mistakes

1. **Importing from `conftest.py`.** Writing `from conftest import sample_user` (or worse, adding it to `sys.path`). It sometimes appears to work, then breaks the moment the file moves or a second `conftest.py` enters the tree, and it completely defeats the auto-discovery design. Fixtures are *requested by name*, never imported.
2. **Dumping every fixture into one giant root `conftest.py`.** Beginners put *all* fixtures at the root "so everything can see them." This makes every fixture global, invites name collisions, slows collection, and destroys the locality that makes overrides useful. The discipline: a fixture lives at the **narrowest** `conftest.py` that covers all its users — push it up only when a second directory genuinely needs it.

---

## STEP 2 — Working example (verified: 4 passed on pytest 9.1.1)

This is a small tree, because `conftest.py` behavior only shows up *across* directories. I built and ran exactly this:

```
demo_conftest/
├── conftest.py            # ROOT: defines base_url + db
├── test_root.py           # sees both root fixtures
├── orders/
│   ├── conftest.py        # OVERRIDES db (most-local wins)
│   └── test_orders.py     # gets orders' db, but root's base_url
└── reports/
    └── test_reports.py    # no local conftest -> gets root db
```

**`demo_conftest/conftest.py`** (root — visible to the whole tree):

```python
"""
ROOT conftest.py  (project-wide fixtures)
Visible to EVERY test at or below this directory, with NO import.
pytest walks UP from each test file collecting conftest.py files.
"""
import pytest


@pytest.fixture
def base_url():
    # Project-wide default. Any test anywhere in the tree can request it.
    return "https://staging.internal"


@pytest.fixture
def db():
    # Pretend this is an expensive shared resource (here: a plain dict).
    return {"env": "root-db", "rows": []}
```

**`demo_conftest/test_root.py`** (no imports — fixtures are injected):

```python
def test_uses_root_fixtures(base_url, db):
    assert base_url == "https://staging.internal"
    assert db["env"] == "root-db"
```

**`demo_conftest/orders/conftest.py`** (child — overrides `db` only):

```python
"""
CHILD conftest.py inside orders/.
Defines a fixture with the SAME NAME as a parent one (`db`).
Rule: the most-LOCAL fixture wins. Tests in orders/ get THIS db,
while `base_url` (only at root) still resolves upward.
"""
import pytest


@pytest.fixture
def db():
    return {"env": "orders-db", "rows": []}
```

**`demo_conftest/orders/test_orders.py`** (proves override + upward resolution):

```python
def test_override_wins(db):
    # Most-local fixture wins: this is orders/ db, NOT the root db.
    assert db["env"] == "orders-db"


def test_parent_still_visible(base_url):
    # base_url isn't overridden here, so it resolves at the ROOT conftest.
    assert base_url == "https://staging.internal"
```

**`demo_conftest/reports/test_reports.py`** (no local conftest → falls through to root):

```python
def test_reports_sees_root_db(db):
    # reports/ has no conftest.py, so `db` resolves at the root.
    assert db["env"] == "root-db"
```

Running `pytest -v` from `demo_conftest/` gives **4 passed**. The two things to *see* here: `test_override_wins` and `test_reports_sees_root_db` request a fixture with the **same name** and get **different objects** — chosen entirely by directory location. Run `pytest --fixtures test_orders.py` and you'll see pytest list the `orders/` `db` shadowing the root one.