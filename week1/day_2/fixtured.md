# Pytest Fixtures - Complete Mental Model

## What Is A Fixture?

A fixture is a reusable dependency managed by pytest.

Instead of creating resources inside tests:

```python
def test_user():
    conn = sqlite3.connect(":memory:")
```

pytest creates resources and injects them into tests:

```python
def test_user(db_connection):
    ...
```

The test receives a ready-to-use object.

This pattern is called Dependency Injection.

---

## Dependency Injection

Consider:

```python
@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")
    yield conn
```

and:

```python
@pytest.fixture
def db_session(db_connection):
    yield db_connection
```

and:

```python
def test_create_user(db_session):
    ...
```

Dependency graph:

```text
test_create_user
        ↓
db_session
        ↓
db_connection
```

Pytest resolves dependencies from the bottom up.

---

## Fixture Resolution

When pytest sees:

```python
def test_create_user(db_session):
```

it thinks:

```text
I need db_session.
```

Then:

```python
def db_session(db_connection):
```

means:

```text
I need db_connection.
```

So pytest executes:

```text
db_connection
        ↓
db_session
        ↓
test_create_user
```

This is called fixture resolution.

---

## Fixtures Are NOT Inheritance

Incorrect mental model:

```text
db_session inherits db_connection
```

Inheritance gives access to methods and attributes.

Example:

```python
class Parent:
    def hello(self):
        pass

class Child(Parent):
    pass
```

Nothing executes automatically.

You must still call:

```python
child.hello()
```

---

Correct mental model:

```text
db_session depends on db_connection
```

Pytest executes the dependency and injects the result.

This is Dependency Injection.

---

## What Gets Injected?

Many beginners think:

```python
def db_session(db_connection):
```

receives:

```python
db_connection()
```

the fixture function.

Incorrect.

It receives:

```python
conn
```

the yielded result.

By the time execution enters:

```python
def db_session(db_connection):
```

the fixture has already executed up to:

```python
yield conn
```

and the parameter contains the yielded object.

Conceptually:

```python
def db_session(conn):
```

is closer to reality.

---

## Yield Fixtures

Fixture:

```python
@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")

    yield conn

    conn.close()
```

Yield fixtures have two phases:

```text
Setup
    ↓
yield
    ↓
Teardown
```

Setup:

```python
conn = sqlite3.connect(...)
```

Teardown:

```python
conn.close()
```

The fixture pauses at yield.

Pytest later resumes it to perform cleanup.

---

## Yield Does NOT Create Resources

Incorrect:

```text
yield conn creates connection
```

Correct:

```text
sqlite3.connect(...) creates connection

yield conn shares connection
```

Think:

```text
Create resource
        ↓
Share resource
        ↓
Cleanup resource
```

---

## What Does `yield db_connection` Mean?

Inside:

```python
def db_session(db_connection):
    yield db_connection
```

Many people think:

```text
Execute db_connection fixture
```

Incorrect.

The fixture already executed.

The statement effectively becomes:

```python
yield conn
```

because:

```python
db_connection == conn
```

at that point.

The yielded object is passed along.

Not the fixture function.

---

## Fixture Scopes

Pytest caches fixtures according to scope.

### Function Scope

Default.

```python
@pytest.fixture
def db():
```

Created once per test.

```text
Test A
    create
    destroy

Test B
    create
    destroy
```

---

### Session Scope

```python
@pytest.fixture(scope="session")
def db():
```

Created once per pytest session.

```text
Session start
    create
    reuse
    reuse
    reuse
Session end
    destroy
```

This is how your `db_connection` fixture works.

---

## Fixture Caching

Important rule:

```text
Need fixture?
        ↓
Already exists for this scope?
        ↓
Yes → reuse
No  → create
```

Example:

```python
@pytest.fixture
def db_session(db_connection):
```

```python
@pytest.fixture
def db_session_2(db_connection):
```

Both receive the same connection object because:

```python
scope="session"
```

causes pytest to cache the result.

The fixture code is not executed again.

---

## Execution Flow For Our Example

Code:

```python
def test_create_user(db_session):
```

Timeline:

```text
Need db_session
        ↓
Need db_connection
        ↓
Create connection
        ↓
Create users table
        ↓
yield conn
        ↓
BEGIN
        ↓
yield conn
        ↓
Run test
        ↓
INSERT Alice
        ↓
SELECT Alice
        ↓
ASSERT
        ↓
ROLLBACK
        ↓
db_session ends
        ↓
(other tests may run)
        ↓
pytest session ends
        ↓
conn.close()
```

---

## Common Misconceptions

### Misconception

```text
Fixtures are inheritance.
```

Reality:

```text
Fixtures use dependency injection.
```

---

### Misconception

```text
Fixture parameters are fixture functions.
```

Reality:

```text
Fixture parameters are fixture results.
```

---

### Misconception

```text
yield creates resources.
```

Reality:

```text
yield shares resources.
```

---

### Misconception

```text
yield db_connection executes db_connection.
```

Reality:

```text
db_connection already executed.

yield db_connection yields the resulting object.
```

---

### Misconception

```text
Session fixtures execute every time they are requested.
```

Reality:

```text
Session fixtures execute once and are reused.
```

---

## Mental Model

Think of fixtures as a dependency graph:

```text
test_create_user
        ↓
db_session
        ↓
db_connection
```

Pytest walks the graph:

```text
Build dependencies
        ↓
Inject results
        ↓
Run test
        ↓
Perform teardown
```

The test does not create resources.

Pytest creates them and injects them.

That is the essence of pytest fixtures.

---

## Interview Questions

### Beginner

What problem do fixtures solve?

Expected Answer:

Reusable setup and teardown of test resources.

---

### Beginner

What design pattern do pytest fixtures implement?

Expected Answer:

Dependency Injection.

---

### Intermediate

When `db_session(db_connection)` executes, what does `db_connection` contain?

Expected Answer:

The yielded fixture result, not the fixture function.

---

### Intermediate

Why is `db_connection` executed before `db_session`?

Expected Answer:

Because `db_session` depends on it.

---

### Advanced

Why does a session-scoped fixture execute only once?

Expected Answer:

Pytest caches fixture results according to scope and reuses them until teardown.