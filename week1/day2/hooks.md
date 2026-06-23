# Pytest Hooks

## What Is a Hook?

A hook is a function that pytest automatically calls at specific points in its lifecycle.

Unlike fixtures, hooks are not requested by tests.

Unlike decorators, hooks are not attached to tests.

Pytest discovers hook functions by name and executes them when a matching event occurs.

Example from our code:

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow-running"
    )
```

The function name is important.

Pytest recognizes:

```python
pytest_configure
```

as a built-in hook and automatically executes it.

---

## Hook vs Fixture

Fixture:

```python
@pytest.fixture
def db_session():
    ...
```

Used when a test requests it:

```python
def test_create_user(db_session):
    ...
```

Pytest creates the fixture because the test asked for it.

---

Hook:

```python
def pytest_configure(config):
    ...
```

Pytest executes it automatically.

No test has to request it.

No decorator is required.

---

## Fixtures vs Hooks - Core Mental Model

One of the most important distinctions in pytest:

```text
Fixtures
---------
Dependency-driven

Need fixture?
    ↓
Resolve dependency
    ↓
Execute fixture
```

Example:

```python
def test_create_user(db_session):
```

Pytest sees:

```text
Need db_session
    ↓
Need db_connection
    ↓
Execute db_connection
    ↓
Execute db_session
    ↓
Run test
```

---

```text
Hooks
------
Event-driven

Event occurs
    ↓
Execute hook
```

Example:

```python
def pytest_configure(config):
```

Pytest sees:

```text
Pytest startup event
    ↓
Execute pytest_configure()
```

Fixtures execute because something depends on them.

Hooks execute because a lifecycle event occurred.

---

## What Happens In Our Example?

Hook:

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow-running"
    )
```

When pytest starts:

```text
pytest starts
    ↓
load configuration
    ↓
execute pytest_configure()
    ↓
collect tests
    ↓
run tests
```

The hook executes once at startup.

---

## What Is The `config` Object?

Pytest passes a configuration object into the hook.

```python
def pytest_configure(config):
```

Think:

```text
config
    ↓
pytest settings
```

This object allows hooks to:

* register markers
* read configuration
* modify settings
* register plugins
* customize behavior

In our example:

```python
config.addinivalue_line(...)
```

updates pytest configuration.

---

## What Does `addinivalue_line()` Do?

Code:

```python
config.addinivalue_line(
    "markers",
    "slow: marks tests as slow-running"
)
```

Conceptually:

```text
Register marker:
    slow
```

This tells pytest:

```text
The marker "slow" is valid.
```

---

## What Are Markers?

A marker is metadata attached to a test.

Example:

```python
@pytest.mark.slow
def test_big_import():
    ...
```

Think:

```text
Test
    ↓
Tag
    ↓
slow
```

The marker itself does not change behavior.

It simply labels the test.

---

## Why Register Markers?

Without registration:

```python
@pytest.mark.slow
def test_big_import():
    ...
```

may produce:

```text
PytestUnknownMarkWarning
```

because pytest does not know whether:

```python
slow
```

is a real marker or a typo.

Registration tells pytest:

```text
slow is a valid marker
```

---

## Does The Hook Create A Decorator?

No.

This was one of the key questions we explored.

The hook:

```python
def pytest_configure(...):
```

does not create:

```python
@pytest.mark.slow
```

Pytest already provides marker decorators.

The hook merely registers metadata describing the marker.

Think:

```text
Hook:
    Register marker

Marker:
    Attach label to test
```

Different responsibilities.

---

## Does The Hook Run Only For Slow Tests?

No.

This is a common misconception.

Our hook:

```python
def pytest_configure(config):
```

runs once per pytest session.

Even if there are no slow tests.

Timeline:

```text
pytest starts
    ↓
pytest_configure()
    ↓
collect tests
    ↓
run tests
```

The hook executes before pytest even knows which tests will run.

---

## Hook Execution Frequency

A common misunderstanding is that all hooks run once.

This is not true.

Hooks execute whenever their associated lifecycle event occurs.

Examples:

```python
def pytest_configure(config):
```

Runs:

```text
Once per pytest session startup
```

Every time you execute:

```bash
pytest
```

a new pytest session is created and `pytest_configure()` runs again.

---

```python
def pytest_runtest_setup(item):
```

Runs:

```text
Before every test
```

---

```python
def pytest_runtest_teardown(item):
```

Runs:

```text
After every test
```

---

```python
def pytest_collection_modifyitems(items):
```

Runs:

```text
During test collection
```

Think:

```text
Event occurs
      ↓
Matching hook executes
```

The execution frequency depends entirely on the hook.

---

## Hooks Are Event Handlers

Think of hooks as event callbacks.

Linux analogy:

```text
Kernel event
    ↓
Callback runs
```

Pytest analogy:

```text
Pytest startup
    ↓
pytest_configure()

Before test
    ↓
pytest_runtest_setup()

After test
    ↓
pytest_runtest_teardown()
```

Hooks execute because an event occurred.

Not because a test requested them.

---

## Can Hooks Read Markers?

Yes.

Some hooks receive information about the test being processed.

Example:

```python
def pytest_runtest_setup(item):
    if "slow" in item.keywords:
        print("Slow test detected")
```

Now the hook can inspect markers.

Important distinction:

```text
Marker does not execute hook.

Hook examines marker.
```

---

## Execution Timeline In Our Example

Full flow:

```text
pytest starts
    ↓
pytest_configure()
        ↓
        register marker "slow"
    ↓
collect tests
    ↓
create fixtures
    ↓
run tests
    ↓
teardown fixtures
    ↓
pytest exits
```

---

## Hook Discovery

How does pytest know to run:

```python
def pytest_configure(...):
```

?

It looks for special hook names.

Conceptually:

```text
pytest starts
    ↓
scan conftest.py
    ↓
find pytest_configure()
    ↓
register hook
    ↓
execute at startup
```

The name itself is the trigger.

---

## Common Misconceptions

### Misconception

```text
Hooks are fixtures.
```

Reality:

```text
Fixtures are requested by tests.

Hooks are called by pytest.
```

---

### Misconception

```text
Hooks are decorators.
```

Reality:

```text
Hooks are event callbacks.
```

---

### Misconception

```text
The hook runs only for marked tests.
```

Reality:

```text
The hook runs once at startup.
```

---

### Misconception

```text
The hook creates @pytest.mark.slow.
```

Reality:

```text
Pytest already provides markers.

The hook registers metadata describing them.
```

---

## Mental Model

Think of hooks as:

```text
Pytest lifecycle events
          ↓
Automatic callback execution
```

Think of fixtures as:

```text
Dependency graph
          ↓
Automatic dependency resolution
```

Comparison:

```text
Fixtures
---------
Need fixture?
    ↓
Resolve dependency
    ↓
Execute fixture

Hooks
------
Event occurs
    ↓
Execute hook
```

Example from our code:

```text
test_create_user
        ↓
db_session
        ↓
db_connection
```

Pytest walks the dependency graph to build fixtures.

---

For hooks:

```text
pytest starts
      ↓
pytest_configure()
      ↓
collect tests
      ↓
run tests
```

Pytest executes hooks when lifecycle events occur.

---

Hooks extend pytest itself.

Fixtures provide resources to tests.

Markers label tests.

These are three separate concepts.

---

### Misconception

```text
Hooks always run once.
```

Reality:

```text
Hook execution frequency depends on the hook.

pytest_configure()
    runs once per pytest session

pytest_runtest_setup()
    runs before every test

pytest_runtest_teardown()
    runs after every test
```

---

### Misconception

```text
Fixtures and hooks solve the same problem.
```

Reality:

```text
Fixtures are dependency-driven.

Hooks are event-driven.
```

---

## Interview Questions

### Beginner

What is a pytest hook?

Expected Answer:

A function automatically called by pytest at specific lifecycle events.

---

### Beginner

How is a hook different from a fixture?

Expected Answer:

Fixtures are requested by tests. Hooks are called automatically by pytest.

---

### Intermediate

When does `pytest_configure()` execute?

Expected Answer:

Once during pytest startup before tests are collected.

---

### Intermediate

Why register markers?

Expected Answer:

To document them and avoid unknown-marker warnings.

---

### Advanced

Does `pytest_configure()` create marker decorators?

Expected Answer:

No. Pytest already provides marker decorators. The hook only registers metadata about the marker.
