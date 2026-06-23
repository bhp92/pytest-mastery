# Pytest Yield Fixtures

## What is `yield`?

A normal `return` immediately terminates a function.

```python
def f():
    return 42
```

Once `return` executes, the function is finished and cannot continue.

`yield` behaves differently.

```python
def f():
    yield 42
```

When `yield` executes:

1. A value is produced.
2. Execution is paused.
3. All local variables and state are preserved.
4. The function can later resume from the exact line after the `yield`.

Think of `yield` as:

> "Here is a value. Pause me. Come back later and I'll continue where I left off."

---

## How Pytest Uses Yield

Pytest uses generators to implement fixtures with setup and teardown logic.

Example:

```python
@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")

    yield conn

    conn.close()
```

The fixture has two phases:

### Setup Phase

Everything before `yield`.

```python
conn = sqlite3.connect(":memory:")
```

This creates resources needed by tests.

### Teardown Phase

Everything after `yield`.

```python
conn.close()
```

This cleans up resources after pytest is finished using them.

---

## What Happens Internally?

Conceptually pytest does something similar to:

```python
g = db_connection()

conn = next(g)          # Run setup until yield

run_tests(conn)         # Tests execute while fixture is paused

next(g)                 # Resume fixture and run teardown
```

The important point is:

```text
yield does not terminate the fixture.

yield pauses the fixture.
```

---

## Execution Flow in Our Example

Fixture:

```python
@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")

    yield conn

    conn.close()
```

Timeline:

```text
Pytest starts
    ↓
Create SQLite connection
    ↓
Create users table
    ↓
yield conn
    ↓
Fixture pauses
    ↓
All tests using db_connection run
    ↓
Pytest reaches end of session
    ↓
Pytest resumes fixture
    ↓
conn.close()
    ↓
Fixture ends
```

---

## IMPORTANT: Common Misconception

Many people assume:

```text
Test finishes
    ↓
Code after yield automatically executes
```

This is not what happens.

The correct sequence is:

```text
Test finishes
    ↓
Pytest resumes/closes generator
    ↓
Code after yield executes
```

The code after `yield` runs because pytest explicitly resumes the paused generator.

The test finishing and the teardown executing are related events, but they are not the same event.

---

## Who Owns the Generator?

With a normal generator:

```python
g = my_generator()
next(g)
next(g)
g.close()
```

You manage the lifecycle.

With a pytest fixture:

```python
@pytest.fixture
def resource():
    yield obj
```

Pytest manages the lifecycle.

Conceptually:

```text
Normal Generator
----------------
You create it.
You resume it.
You close it.

Pytest Yield Fixture
--------------------
You define it.
Pytest resumes it.
Pytest closes it.
```

The test author never calls:

```python
next(...)
close(...)
```

Pytest does all of that automatically.

---

## Exception Safety

Pytest guarantees teardown execution even if tests fail.

Example:

```python
def test_boom(db_connection):
    raise RuntimeError("Oops")
```

Timeline:

```text
Setup
    ↓
yield conn
    ↓
Test crashes
    ↓
Pytest performs teardown
    ↓
conn.close()
```

This is conceptually similar to:

```python
try:
    run_test()
finally:
    cleanup()
```

---

## Single-Yield Rule

A pytest yield fixture must yield exactly once.

Valid:

```python
@pytest.fixture
def resource():
    setup()

    yield obj

    teardown()
```

Invalid:

```python
@pytest.fixture
def resource():
    yield obj1
    yield obj2
```

Pytest expects a single handoff point:

```text
setup
    ↓
yield resource
    ↓
tests run
    ↓
teardown
```

Multiple yields are valid in normal Python generators but not in pytest yield fixtures.

---

## Yield vs Transaction

These are separate concepts.

Yield:

```python
yield conn
```

Transaction:

```python
db_connection.execute("BEGIN")
...
db_connection.execute("ROLLBACK")
```

Yield controls fixture execution.

Transactions control database changes.

Do not confuse the two.

```text
yield
    ↓
Pause fixture execution

BEGIN
    ↓
Start tracking database changes
```

They solve completely different problems.

---

## Mental Model

Think of a yield fixture as:

```text
Setup Resource
      ↓
Hand Resource To Test
      ↓
Pause Fixture
      ↓
Test Uses Resource
      ↓
Pytest Returns To Fixture
      ↓
Cleanup Resource
```

Or in plain English:

> "Here is the resource. Pause me. When you're done, come back and I'll continue exactly where I left off."

---

## Interview Questions

### Beginner

Why use `yield` instead of `return` in a fixture?

Expected answer:

`yield` allows setup code before the yield and teardown code after the yield.

---

### Intermediate

When does the code after `yield` execute?

Expected answer:

When pytest resumes or closes the paused fixture generator during teardown.

---

### Intermediate

Does the code after `yield` execute automatically because the test finished?

Expected answer:

No. It executes because pytest explicitly resumes or closes the generator after the test finishes.

---

### Advanced

Why is a yield fixture safer than manually calling cleanup functions?

Expected answer:

Pytest guarantees teardown execution even when tests fail or raise exceptions.