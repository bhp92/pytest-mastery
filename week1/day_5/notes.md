# 🧪 Week 1, Day 5 — Organizing Test Files

### What it is and why it exists

Test organization is how you lay out your test files, directories, and package markers (`__init__.py`) so that pytest reliably **(a)** finds every test, **(b)** imports them without name collisions, and **(c)** exercises the package your users will actually install — not a lucky copy sitting on your local path.

It exists because layout stops being cosmetic the moment a suite grows past one directory. Bad layout produces two nasty, silent-ish failures: tests that quietly never run, and a hard collection error (`import file mismatch`) that blocks the *entire* suite over a filename clash. Both are pure structure problems, not test-logic problems — which is exactly why interviewers use them to separate people who've only written toy tests from people who've maintained a real suite.

### Key concepts

**1. Flat layout vs `src/` layout.** In a *flat* layout your package sits at the repo root (`shop/` next to `tests/`). The repo root is on `sys.path`, so `import shop` works even if you never installed the package — convenient, but it *masks packaging bugs*. In a *`src/` layout* the package lives under `src/shop/`, and the repo root is **not** importable, so you must `pip install -e .` first. That one constraint forces your tests to import the *installed* package — the same artifact your users get — so a missing `__init__.py`, a module you forgot to include in the wheel, or missing package data all fail loudly in tests instead of in production.

Don't let your tests accidentally rely on your repository structure. Make them rely on the installed package, because that's what your users will actually have. `pip install -e .` installs the project according to pyproject.toml. If pyproject.toml excludes a module/package (e.g., shop.payment), then import shop.payment fails with ModuleNotFoundError even if src/shop/payment.py physically exists. Only what the packaging configuration exposes is importable.

It forces your tests to use the installed package instead of the repository layout, so packaging mistakes are caught during development. If a user wouldn't be able to import a package after installing your project, your tests shouldn't be able to import it either. Make the development environment behave like the user's environment. If a package can't be imported after installation in production, the tests should fail during development instead of after release.

**2. Where `tests/` lives.** The modern default is a `tests/` directory *outside* the package (sibling to `src/`). Putting tests *inside* the package (`shop/tests/`) means they ship to end users in the wheel — only do that deliberately.

**3. `__init__.py` in test directories — the subtle one.** pytest's default import mode is `prepend`: it prepends each test file's rootdir to `sys.path` and imports the file **by its basename**. Consequence: every test file needs a **unique basename across the whole suite**. `tests/api/test_utils.py` and `tests/db/test_utils.py` collide → `import file mismatch`. You have three ways out: give files unique names, add `__init__.py` files to make tests a real package (so they import as `api.test_utils` vs `db.test_utils`), or — the current recommended answer — set `import-mode=importlib`, which imports each test as a distinct module without touching `sys.path` and needs no `__init__.py` at all. Knowing that `importlib` is the 2020s answer (vs the old `__init__.py` workaround) is a senior-level signal.

Python remembers imported modules in sys.modules. It identifies them by their import name, not by their file path. In pytest's default (prepend) mode, test files are imported using only their basename (e.g., test_utils), not their full path (api.test_utils or db.test_utils). So if two test files have the same basename, Python thinks they are the same module, causing a collision.

Solution 2 — __init__.py

Adding __init__.py makes the test directories real Python packages. Pytest then imports test files using their full package path (e.g., api.test_utils and db.test_utils) instead of just their basename (test_utils), preventing module name collisions.

Solution 3 — import-mode=importlib (Recommended)

import-mode=importlib makes pytest load each discovered test file directly from its file path using Python's importlib, assigning each test a unique internal module identity. This avoids sys.modules name collisions without requiring __init__.py or unique filenames.

**4. `conftest.py` as an organizing tool.** Fixture *scope follows directory hierarchy*: a fixture in `tests/conftest.py` is visible everywhere; one in `tests/integration/conftest.py` is visible only under `integration/`. Nested conftests are how you keep fixtures near the tests that use them instead of one god-file — you already have this in your Day 2 notes; Day 5 is where it becomes a *layout* decision.

**5. `rootdir` & `testpaths`.** pytest anchors a `rootdir` from your config file + invocation, and `testpaths` in `pytest.ini` scopes discovery (e.g. away from `node_modules/`, vendored deps, build artifacts).

### One real-world production example

A service repo in `src/` layout:

```
myservice/
├── pyproject.toml            # [tool.pytest.ini_options] import-mode = "importlib"
├── src/
│   └── myservice/
│       ├── __init__.py
│       ├── orders.py
│       └── payments.py
└── tests/
    ├── conftest.py           # shared fixtures (db, fake clock)
    ├── unit/
    │   └── test_payments.py
    └── integration/
        ├── conftest.py       # fixtures ONLY integration tests see (real DB)
        └── test_payments.py  # ← same basename as unit/test_payments.py
```

Two files named `test_payments.py` coexist because of `import-mode=importlib` (or `__init__.py`), and CI runs `pip install -e . && pytest` so the suite tests the *built* package. This is the same fast-gate / slow-gate promotion pattern from your DevOps CI/CD notes — `pytest -m unit` gates the PR, `pytest -m integration` gates the deploy.

### The 2 most common beginner mistakes

**1. Duplicate test filenames with no package markers.** Two `test_utils.py` in different folders under default `prepend` mode gives the confusing `import file mismatch: imported module 'test_utils' has this __file__ attribute ... which is not the same as the test file we want to collect`. Beginners think pytest is broken; it's a layout collision. (I reproduced this above — you'll reproduce it yourself in Task 2.)

**2. Trusting a flat layout so tests pass locally but the package is broken when installed.** A submodule not listed in `packages`, or a missing `__init__.py`, still imports fine in flat layout because the repo root is on `sys.path` — so green tests hide a broken wheel. `src/` layout catches it because nothing imports until you install.

---

### Working Example

This is the live experiment I just ran (real output, not illustrative). It's the heart of today's topic — the duplicate-basename collision and its two fixes:

```bash
# tests/api/test_utils.py  ->  def test_api_thing(): assert True
# tests/db/test_utils.py   ->  def test_db_thing():  assert True
# Same basename, different dirs, no __init__.py.

$ python -m pytest -q          # default (prepend) import mode
==================================== ERRORS ====================================
___________________ ERROR collecting tests/db/test_utils.py ____________________
import file mismatch:
imported module 'test_utils' has this __file__ attribute:
  /tmp/orgdemo/tests/api/test_utils.py
which is not the same as the test file we want to collect:
  /tmp/orgdemo/tests/db/test_utils.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename ...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!

# FIX A — make tests a package (add __init__.py to tests/, api/, db/):
$ python -m pytest -q
..                                                                       [100%]
2 passed in 0.01s

# FIX B — leave __init__.py out, switch import mode instead:
$ python -m pytest -q --import-mode=importlib
..                                                                       [100%]
2 passed in 0.01s
```

The takeaway to internalize: the *same two test files* go from a hard collection error to green **without changing a line of test code** — only the layout/import strategy changed. That's the whole thesis of Day 5.

---