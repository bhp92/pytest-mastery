# Pytest Fixtures and Dependency Injection

## What Is Dependency Injection?

Dependency Injection (DI) is a design pattern where an object receives its dependencies from an external system rather than creating them itself.

Without dependency injection:

```python
def create_user():
    conn = sqlite3.connect(":memory:")
```

The function creates its own dependency.

With dependency injection:

```python
def create_user(conn):
    ...
```

The dependency is provided from outside.

The function does not know:

* how the dependency was created
* when it was created
* who created it

It simply uses it.

---

## Pytest Fixtures Are Dependency Injection

Consider:

```python
@pytest.fixture(scope="session")
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

Dependency chain:

```text
test_create_user
        ↓
depends on
        ↓
db_session
        ↓
depends on
        ↓
db_connection
```

Pytest resolves the entire chain automatically.

---

## The Most Important Mental Model

Many beginners think:

```text
db_session inherits db_connection
```

This is incorrect.

Many beginners also think:

```text
db_session calls db_connection
```

This is also incorrect.

What actually happens:

```text
db_session depends on db_connection
        ↓
pytest executes db_connection
        ↓
pytest injects the result
        ↓
db_session receives the object
```

This is dependency injection.

---

## Inheritance vs Dependency Injection

### Inheritance

```python
class Database:
    def connect(self):
        print("connecting")

class UserDB(Database):
    pass
```

Usage:

```python
db = UserDB()
db.connect()
```

Important:

```text
Methods become available.

Nothing executes automatically.
```

The child receives access to behavior.

The child still chooses when to execute it.

---

### Dependency Injection

```python
def use_db(conn):
    ...
```

Usage:

```python
conn = create_connection()

use_db(conn)
```

Important:

```text
Dependency already exists.

Dependency is passed in.
```

The consumer receives a ready-to-use object.

---

## Understanding Our Example

Fixture:

```python
@pytest.fixture(scope="session")
def db_connection():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")

    yield conn

    conn.close()
```

Execution:

```text
Create connection
        ↓
Create table
        ↓
yield conn
        ↓
Fixture pauses
```

At this point:

```text
Connection already exists.
```

---

## What Does `yield conn` Actually Do?

Many people assume:

```text
yield conn
```

creates the connection.

This is incorrect.

The connection was created earlier:

```python
conn = sqlite3.connect(":memory:")
```

The yield simply hands the already-created object to pytest.

Think:

```text
Create connection
        ↓
Share connection
        ↓
Cleanup connection later
```

Not:

```text
Share connection
        ↓
Create connection
```

---

## Understanding Fixture Parameters

Consider:

```python
@pytest.fixture
def db_session(db_connection):
```

A common misconception:

```text
db_connection refers to the fixture function
```

This is incorrect.

By the time execution enters `db_session`:

```text
db_connection fixture already executed
```

The parameter contains:

```python
conn
```

the yielded SQLite connection object.

Conceptually:

```python
def db_session(conn):
```

would be a closer representation.

---

## What Does `yield db_connection` Mean?

Inside:

```python
@pytest.fixture
def db_session(db_connection):
    yield db_connection
```

Many people think:

```text
Execute db_connection fixture
```

This is incorrect.

The fixture already executed.

The statement actually means:

```python
yield conn
```

which simply passes the connection object to the test.

---

## Internal Execution Flow

Pytest conceptually does something similar to:

```python
g1 = db_connection()

conn = next(g1)

g2 = db_session(conn)

session = next(g2)

test_create_user(session)
```

Notice:

```text
db_session receives conn

not

db_connection()
```

The fixture result is injected.

---

## Full Timeline For Our Example

```text
test_create_user starts
        ↓
Needs db_session
        ↓
db_session needs db_connection
        ↓
Execute db_connection
        ↓
Create SQLite connection
        ↓
Create users table
        ↓
yield conn
        ↓
Execute db_session
        ↓
BEGIN
        ↓
yield conn
        ↓
Run test
        ↓
ROLLBACK
        ↓
db_session ends
        ↓
Other tests may run
        ↓
Session ends
        ↓
conn.close()
```

---

## Why This Feels Strange

Most Python code looks like:

```python
result = some_function()
```

You explicitly call functions.

Fixtures work differently.

You write:

```python
def test_create_user(db_session):
```

and pytest interprets:

```text
I know a fixture called db_session.
I'll build it and inject it.
```

No explicit function call is visible.

This is dependency injection.

---

## Linux Analogy

Inheritance:

```text
Parent process
        ↓
Child inherits capabilities
```

The child still chooses what to execute.

Dependency Injection:

```text
Request running database
        ↓
System starts database
        ↓
System hands you connection
```

You receive a ready-to-use resource.

---

## Common Misconceptions

### Misconception

```text
db_session inherits db_connection
```

Reality:

```text
db_session depends on db_connection.
```

---

### Misconception

```text
db_session calls db_connection.
```

Reality:

```text
pytest executes db_connection and injects the result.
```

---

### Misconception

```text
yield conn creates the connection.
```

Reality:

```text
sqlite3.connect() creates the connection.

yield only shares it.
```

---

### Misconception

```text
yield db_connection executes the fixture.
```

Reality:

```text
The fixture already executed.

yield db_connection passes the resulting object.
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

## Mental Model

Think of pytest fixtures as:

```text
Dependency Graph
----------------

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

The test never creates the dependencies itself.

Pytest creates them and injects them.

That is Dependency Injection.

---

## Interview Questions

### Beginner

What design pattern do pytest fixtures implement?

Expected Answer:

Dependency Injection.

---

### Beginner

Does `db_session` inherit from `db_connection`?

Expected Answer:

No. It depends on `db_connection`.

---

### Intermediate

When `db_session(db_connection)` executes, what does the parameter contain?

Expected Answer:

The yielded result of the `db_connection` fixture, not the fixture function itself.

---

### Intermediate

Does `yield db_connection` execute the fixture?

Expected Answer:

No. The fixture has already executed. The statement yields the resulting object.

---

### Advanced

Why is dependency injection useful?

Expected Answer:

It decouples resource creation from resource usage, improves testability, and allows frameworks like pytest to manage setup and teardown automatically.
