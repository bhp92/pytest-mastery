# Week 6 — Real-World & CI

**Goal:** Ship a production-grade test suite. This is your capstone week.

---

## Day 1 — Testing Django/Flask Apps (40 min)

```bash
pip install pytest-django
```

Key fixtures from `pytest-django`:
- `client` — Django test client (no auth)
- `admin_client` — logged in as admin
- `rf` — Django RequestFactory
- `db` — allows DB access (per test, rolled back)
- `transactional_db` — real transactions (for testing atomic blocks)

```python
# conftest.py for Django
import django
from django.conf import settings

def pytest_configure():
    settings.configure(
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth", "myapp"],
    )
```

---

## Day 2 — Testing HTTP APIs (40 min)

```bash
pip install responses pytest-httpx
```

```python
import responses

@responses.activate
def test_external_api():
    responses.add(responses.GET, "https://api.example.com/users/1",
                  json={"id": 1, "name": "Alice"}, status=200)
    result = fetch_user(1)
    assert result["name"] == "Alice"
```

---

## Day 3 — GitHub Actions CI (40 min)

See `.github/workflows/tests.yml` in the repo root.

Key flags for CI:
```bash
pytest --junitxml=results.xml   # for test result reporting
pytest -n auto                   # parallel across CPU cores
pytest --cov --cov-fail-under=80 # fail CI if coverage drops
```

---

## Day 4 — Performance & Debugging (40 min)

```bash
pytest --durations=10            # show 10 slowest tests
pytest -s                        # show print/log output
pytest --pdb                     # drop into debugger on failure
pytest --lf                      # re-run only last failed
pytest --tb=long                 # full traceback
```

---

## Day 5 — Capstone Project (40 min)

Build a complete test suite for `week6/app.py` (a small CRUD app).

Requirements:
- [ ] At least 15 tests across all layers
- [ ] Use fixtures with at least 2 different scopes
- [ ] Use parametrize for at least one test
- [ ] Mock at least one external dependency
- [ ] Achieve 85%+ branch coverage
- [ ] All tests pass in < 5 seconds

```bash
pytest week6/ --cov=week6 --cov-branch --cov-report=html --durations=5
open htmlcov/index.html
```
