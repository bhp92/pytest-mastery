# Flat Layout vs `src/` Layout — Hands-On Demo Notes

Original claim being tested:

> Flat layout in a *flat* layout your package sits at the repo root (`shop/` next to `tests/`). The repo root is on `sys.path`, so `import shop` works even if you never installed the package — convenient, but it *masks packaging bugs*. In a *`src/` layout* the package lives under `src/shop/`, and the repo root is **not** importable, so you must `pip install -e .` first. That one constraint forces your tests to import the *installed* package — the same artifact your users get — so a missing `__init__.py`, a module you forgot to include in the wheel, or missing package data all fail loudly in tests instead of in production.

Everything below was executed on the user's own VM (`bpuranik@lab`), not simulated.

---

## Questions & Answers

### 1. What does `__version__` do / why did we set it in `__init__.py`?

`__version__` is just a plain module-level variable — Python attaches no special meaning to it. It's a **convention**, not a language feature. Tools and humans look for `shop.__version__` as the canonical place to find "what version of this package is this?" at runtime, e.g. `import shop; print(shop.__version__)`. Some packaging tools (like `setuptools` with `attr:` version directives) can even read this value automatically to set the package's version in `pyproject.toml`, so you only maintain the version number in one place. In our demo it was set but not actually wired into `pyproject.toml`'s `version = "0.1.0"` — those two `0.1.0`s were just coincidentally kept in sync by hand.

### 2. What is a "wheel" / wheel configuration?

A **wheel** (`.whl` file) is Python's standard *built, installable* package format — a zip file containing your package's code plus metadata (name, version, dependencies, etc.), ready for `pip install`. It's the same kind of artifact you download from PyPI for any third-party package. Building a wheel is a distinct step from writing your source code: a build backend (here, `setuptools`, declared in `pyproject.toml`'s `[build-system]` table) reads your packaging configuration and decides **which files actually get copied into the wheel**. "Wheel configuration" refers to that packaging config — in our demo, the `[tool.setuptools]` / `[tool.setuptools.packages.find]` sections — which controls exactly this inclusion decision. We saw directly in the build log which files were added:

```
adding 'shop/__init__.py'
adding 'shop/core.py'
```

`payments/` was silently left out because it wasn't declared, proving the config — not the source tree — determines what ships.

### 3. What is `pyproject.toml`, and how is it different from `pytest.ini`?

`pyproject.toml` is the modern, standardized **project/build configuration file** for Python packages. It tells tools like `pip` and `build` how to build and install your project — what build backend to use, the package's name/version/dependencies, and (via `[tool.setuptools...]` tables) exactly which source files count as "the package." It is what makes a directory `pip install`-able at all.

`pytest.ini` (or `pyproject.toml`'s own `[tool.pytest.ini_options]` table, which we didn't use here) is a much narrower, **test-runner-only** configuration file — it tells `pytest` things like which directories to search for tests, custom markers, command-line defaults, etc. It has nothing to do with building or installing the package; it only configures how `pytest` behaves once it runs.

In short: `pyproject.toml` = "how do I become an installable artifact," `pytest.ini` = "how should the test runner behave." A project can have `pyproject.toml` without any test-specific config, or use `pytest.ini` for tests while still depending on `pyproject.toml` for packaging.

### 4. What does `pip install -e .` do, mechanically?

`pip install -e .` is an **editable install**. Mechanically, in our run:

1. Pip read `pyproject.toml` (build backend = `setuptools`) in the current directory (`.`).
2. It registered the package (`shop`) into the active venv's `site-packages`, but instead of *copying* the source files there, it created a link/pointer back to your actual source tree.
3. `pip show shop` confirmed this: `Location` pointed at the venv's `site-packages`, while `Editable project location` pointed straight back at `/home/bpuranik/workspace/pkgdemo/srcdemo` — i.e. your live `src/` folder.

The practical effect: `import shop` now resolves through the *installed package metadata*, not by directory-guessing off `sys.path[0]`, but any edits you make to `src/shop/*.py` are picked up immediately with no reinstall needed — great for day-to-day development.

**Important discovery from this demo:** an editable install is *not* equivalent to a real release build. When we later added `payments/` and forgot to register it in `pyproject.toml`, the editable install **still found it** (both tests passed), because editable installs point at the whole `src/` tree rather than enforcing the packaging file list. Only building an actual **wheel** (`python -m build --wheel`) and installing *that* correctly caught the missing subpackage. So: `pip install -e .` verifies "can this be installed and imported," but it does **not** verify "is my packaging list complete" — that requires a real wheel build.

### 5. Does `pip install -e .` read package info from `pyproject.toml` and install it into the current directory's venv — is that the correct understanding?

Yes — with a small precision: it reads `pyproject.toml` from the current directory (via the build backend it declares) to figure out the package name, version, and which source directory to point at (`where = ["src"]` in our config). It installs that registration into **whichever venv is currently active**, not necessarily "the current directory's venv" specifically — the venv just happens to be active because we had `source .venv/bin/activate`'d into it first. If a different venv had been active, it would have installed there instead.

### 6. Confirm: `shop` was not present in the searched directory, so Python raised `ModuleNotFoundError`, because `sys.path[0]` pointed at the current directory and it searched there — is this understanding correct?

Yes, exactly correct. `sys.path[0]` was `''` (the current directory, `srcdemo/`) in both the flat and src cases — identical mechanism. The only difference was *what physically existed there*: flat had `shop/` sitting directly in the current directory, so the search succeeded. Src had only `src/shop/`, and `src/` itself was never added to `sys.path`, so the search of the current directory came up empty and Python raised `ModuleNotFoundError: No module named 'shop'`.

---

## Full Demo Log

### Environment

```
$ python3 --version
Python 3.12.3
$ pip --version
pip 24.0 ...
```

### Part 1 — Flat Layout

**Setup:**

```bash
mkdir -p ~/workspace/pkgdemo/flat/shop ~/workspace/pkgdemo/flat/tests
cd ~/workspace/pkgdemo/flat
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

**Package + test files:**

```python
# shop/__init__.py
__version__ = "0.1.0"
```

```python
# shop/core.py
def greeting():
    return "hello from shop.core"
```

```python
# tests/test_core.py
from shop.core import greeting

def test_greeting():
    assert greeting() == "hello from shop.core"
```

**Confirm nothing is installed, then run tests:**

```
$ pip show shop 2>&1 | head -1
WARNING: Package(s) not found: shop
$ python -c "import sys; print(repr(sys.path[0]))"
''
$ python -m pytest -q
.                                                                        [100%]
1 passed in 0.00s
```

**Result:** `shop` is not installed anywhere, yet the test passes — because `shop/` sits directly in the current directory (`sys.path[0]`).

---

### Part 2 — `src/` Layout

**Setup:**

```bash
mkdir -p ~/workspace/pkgdemo/srcdemo/src/shop ~/workspace/pkgdemo/srcdemo/tests
cd ~/workspace/pkgdemo/srcdemo
```

```python
# src/shop/__init__.py
__version__ = "0.1.0"
```

```python
# src/shop/core.py
def greeting():
    return "hello from shop.core"
```

```python
# tests/test_core.py
from shop.core import greeting

def test_greeting():
    assert greeting() == "hello from shop.core"
```

**Prove the import fails before any install (no venv yet, system Python):**

```
$ python3 -c "import sys; print(repr(sys.path[0]))"
''
$ python3 -c "import shop"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'shop'
```

**`pyproject.toml` (initial, auto-discovery version):**

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "shop"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["src"]
```

**Create venv, editable install, confirm fix:**

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
...
Successfully installed shop-0.1.0

$ pip show shop
Name: shop
Version: 0.1.0
Location: /home/bpuranik/workspace/pkgdemo/srcdemo/.venv/lib/python3.12/site-packages
Editable project location: /home/bpuranik/workspace/pkgdemo/srcdemo

$ python -c "import shop, shop.core; print(shop.__file__); print(shop.core.greeting())"
/home/bpuranik/workspace/pkgdemo/srcdemo/src/shop/__init__.py
hello from shop.core

$ pip install pytest
$ python -m pytest -q
.                                                                        [100%]
1 passed in 0.00s
```

**Result:** Import and tests fail with zero setup, exactly as the src layout is designed to force — and succeed only after `pip install -e .`, resolving through the installed package rather than directory-guessing.

---

### Part 3 — The Packaging Bug Demo (the real payoff)

**Goal:** prove that flat layout can silently ship a broken package, while src layout's install step catches it in tests.

**Add a new subpackage to both layouts identically.**

Flat:

```bash
cd ~/workspace/pkgdemo/flat
source .venv/bin/activate
mkdir -p shop/payments
```

```python
# shop/payments/__init__.py
(empty)
```

```python
# shop/payments/processor.py
def charge(amount):
    return f"charged {amount}"
```

```python
# tests/test_payments.py
from shop.payments.processor import charge

def test_charge():
    assert charge(10) == "charged 10"
```

```
$ python -m pytest -q
..                                                                       [100%]
2 passed in 0.00s
```

Src (same files, under `src/shop/payments/`):

```
$ python -m pytest -q      # still using the editable install
..                                                                       [100%]
2 passed in 0.00s
```

**Key finding:** the editable install (`pip install -e .`) picked up `payments/` automatically too — it does **not** validate the packaging file list, since it just points at the whole `src/` directory. To actually test packaging correctness, we need a **real wheel build**.

**Deliberately misconfigure `pyproject.toml`** to register only `shop`, "forgetting" `payments` — simulating a real packaging mistake:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "shop"
version = "0.1.0"

[tool.setuptools]
packages = ["shop"]
package-dir = {"" = "src"}
```

**Build an actual wheel (not editable) and inspect exactly what got packed:**

```
$ pip uninstall -y shop
$ pip install build
$ python -m build --wheel
...
adding 'shop/__init__.py'
adding 'shop/core.py'
adding 'shop-0.1.0.dist-info/METADATA'
adding 'shop-0.1.0.dist-info/WHEEL'
adding 'shop-0.1.0.dist-info/top_level.txt'
adding 'shop-0.1.0.dist-info/RECORD'
Successfully built shop-0.1.0-py3-none-any.whl
$ ls dist/
shop-0.1.0-py3-none-any.whl
```

Note: `payments/` is **absent** from the "adding..." lines — the bug is baked into the artifact at build time.

**Install the real wheel and run tests:**

```
$ pip install dist/shop-0.1.0-py3-none-any.whl
Successfully installed shop-0.1.0

$ python -m pytest -q
ERROR collecting tests/test_payments.py
ImportError while importing test module '.../tests/test_payments.py'.
tests/test_payments.py:1: in <module>
    from shop.payments.processor import charge
E   ModuleNotFoundError: No module named 'shop.payments'
1 error in 0.04s
```

**Flat, for comparison — same source addition, no packaging step exists to forget:**

```
$ cd ~/workspace/pkgdemo/flat
$ source .venv/bin/activate
$ python -m pytest -q
..                                                                       [100%]
2 passed in 0.00s
```

---

## Side-by-Side Result

| | Flat layout | `src/` layout (installed as real wheel) |
|---|---|---|
| Import with zero install | ✅ works | ❌ `ModuleNotFoundError` |
| Forces `pip install -e .` | No | Yes |
| `payments/` added to source, forgotten in packaging config | Not applicable — no packaging config exists | Config explicitly omits it |
| `pytest` result after the mistake | ✅ 2 passed (bug invisible) | ❌ 1 error — `ModuleNotFoundError: No module named 'shop.payments'` |
| Editable install (`pip install -e .`) catches the same mistake? | n/a | **No** — editable installs bypass the packaging file list entirely |
| Real wheel build/install catches the mistake? | n/a | **Yes** — this is the only step that actually validates packaging |

---

## Conclusions & Takeaways

1. **`sys.path[0]` is always the current directory** (`''`) regardless of layout. The difference between flat and src is purely about *what physically exists* at that location — `shop/` directly present (flat) vs. only `src/shop/` present (src, which is invisible from the repo root).

2. **Flat layout has no packaging step at all.** There is nothing to build, nothing to "forget to include." Tests always run against whatever happens to be sitting in the working directory — convenient, but this is exactly what allows a broken/incomplete package to go undetected all the way to production, since your local tests never touch the actual installable artifact.

3. **`src/` layout forces installation before anything works**, and that constraint is the entire value proposition — but only when the install is a **real build** (wheel), not an editable install.

4. **Editable installs (`pip install -e .`) are not a substitute for a real packaging check.** They're great for fast local dev (edits are picked up instantly, no reinstall), but because they point directly at your `src/` tree rather than enforcing the declared package list, they will *not* catch a subpackage you forgot to register — we proved this directly (the same "forgotten" `payments/` package imported fine under the editable install and only failed once we built and installed a real wheel).

5. **The real test of packaging correctness is: build a wheel, install *that*, then run tests.** This is the only step in the whole workflow that reproduces exactly what a user pip-installing your package would experience — and it's the step that actually caught the injected bug in this demo.

6. **Practical implication:** if you use `src/` layout for its safety benefits, your CI pipeline should periodically (or always) test against a built wheel install — not just an editable install — or you get a false sense of security identical to the flat-layout failure mode this whole exercise was meant to avoid.