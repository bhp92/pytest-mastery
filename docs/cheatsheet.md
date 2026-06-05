# Pytest Cheat Sheet

## Running Tests

```bash
pytest                          # run all tests
pytest -v                       # verbose output
pytest -s                       # show print/log output
pytest -x                       # stop on first failure
pytest --lf                     # re-run last failed only
pytest --ff                     # run failed first, then rest
pytest -k "keyword"             # run tests matching keyword
pytest -m slow                  # run tests with @pytest.mark.slow
pytest -m "not slow"            # skip slow tests
pytest --tb=short               # shorter tracebacks
pytest --tb=no                  # no tracebacks
pytest --durations=10           # show 10 slowest tests
pytest -n auto                  # parallel (pytest-xdist)
pytest --pdb                    # drop into debugger on fail
pytest --co -q                  # list collected tests (dry run)
```

## Coverage

```bash
pytest --cov=myapp                     # basic coverage
pytest --cov=myapp --cov-branch        # branch coverage
pytest --cov-report=html               # HTML report → htmlcov/
pytest --cov-report=term-missing       # show uncovered lines
pytest --cov-fail-under=80             # fail if < 80%
```

## Fixtures — Quick Reference

```python
@pytest.fixture                    # function scope (default)
@pytest.fixture(scope="class")     # per test class
@pytest.fixture(scope="module")    # per test file
@pytest.fixture(scope="session")   # once per test run
@pytest.fixture(autouse=True)      # run for every test automatically

@pytest.fixture
def my_fixture():
    # setup
    yield value
    # teardown (always runs, even if test fails)
```

## Parametrize

```python
@pytest.mark.parametrize("x, y, expected", [
    (1, 2, 3),
    (0, 0, 0),
    pytest.param(-1, 1, 0, id="negatives"),
    pytest.param(None, 1, None, marks=pytest.mark.xfail),
])
def test_add(x, y, expected):
    assert add(x, y) == expected
```

## Marks

```python
@pytest.mark.skip(reason="...")
@pytest.mark.skipif(condition, reason="...")
@pytest.mark.xfail(reason="...", strict=True)
@pytest.mark.slow                  # custom mark (register in pytest.ini)
@pytest.mark.parametrize(...)
```

## Mocking

```python
# pytest-mock (mocker fixture)
def test_example(mocker):
    mock = mocker.patch("myapp.module.function")
    mock.return_value = 42
    mock.side_effect = ValueError("boom")
    mocker.patch.object(obj, "method")
    mocker.patch.dict(os.environ, {"KEY": "val"})

# monkeypatch
def test_example(monkeypatch):
    monkeypatch.setattr(obj, "attr", value)
    monkeypatch.setenv("KEY", "value")
    monkeypatch.delenv("KEY", raising=False)
    monkeypatch.setitem(dict_, "key", value)
```

## Assertions

```python
with pytest.raises(ValueError, match=r"regex"):
    risky_call()

with pytest.warns(DeprecationWarning):
    legacy_call()

# Approx for floats
assert 0.1 + 0.2 == pytest.approx(0.3)
assert [0.1, 0.2] == pytest.approx([0.1, 0.2], abs=1e-6)
```

## pytest.ini Options

```ini
[pytest]
addopts = --tb=short -v
markers =
    slow: slow integration tests
    unit: fast unit tests
testpaths = tests
asyncio_mode = auto
```
