# Pytest Database Transactions and Test Isolation

## What Are BEGIN and ROLLBACK?

`BEGIN` and `ROLLBACK` are SQL transaction statements.

They are part of the database engine (SQLite in our example), not Python language features.

Example:

```python
db_connection.execute("BEGIN")
```

This sends the SQL statement:

```sql
BEGIN;
```

to SQLite.

Similarly:

```python
db_connection.execute("ROLLBACK")
```

sends:

```sql
ROLLBACK;
```

to SQLite.

The Python `execute()` method acts as a messenger between Python and the database engine.

---

## What Is a Transaction?

A transaction is a temporary unit of work that groups database changes together.

During a transaction, changes are tracked and can later be:

```text
COMMIT   -> Save changes permanently
ROLLBACK -> Discard all changes
```

Conceptually:

```text
BEGIN
    INSERT Alice
    UPDATE Bob
    DELETE Charlie
COMMIT
```

Result:

```text
All changes saved.
```

Or:

```text
BEGIN
    INSERT Alice
    UPDATE Bob
    DELETE Charlie
ROLLBACK
```

Result:

```text
No changes persisted.
```

---

## What Does BEGIN Actually Do?

When SQLite receives:

```sql
BEGIN;
```

it starts tracking database changes made through that connection.

Think:

```text
Database
    ↓
BEGIN
    ↓
Start recording changes
```

Nothing visible changes immediately.

The transaction simply becomes active.

---

## What Does ROLLBACK Actually Do?

When SQLite receives:

```sql
ROLLBACK;
```

it discards all changes made since the matching `BEGIN`.

Think:

```text
BEGIN
    ↓
Make changes
    ↓
ROLLBACK
    ↓
Discard changes
```

It is as if those changes never happened.

---

## Important: Transactions Do NOT Create a New Database

A common misconception is:

```text
BEGIN
```

creates:

```text
New database
New connection
New namespace
```

This is incorrect.

Transactions operate on the existing database connection.

They do not create:

* a new database
* a new connection
* a new SQLite instance
* a namespace

They simply track changes made through the current connection.

Conceptually:

```text
Connection
    ↓
BEGIN
    ↓
Track changes on this connection
```

---

## Relationship to Our Fixture

Fixture:

```python
@pytest.fixture
def db_session(db_connection):
    db_connection.execute("BEGIN")

    yield db_connection

    db_connection.execute("ROLLBACK")
```

Execution flow:

```text
Start transaction
    ↓
yield db_connection
    ↓
Test executes
    ↓
Test inserts/updates/deletes rows
    ↓
Pytest resumes fixture
    ↓
ROLLBACK
    ↓
Changes discarded
```

The transaction remains active while the test runs.

---

## Yield Does NOT Start the Transaction

A common misconception is:

```text
yield starts the transaction
```

This is incorrect.

The transaction starts here:

```python
db_connection.execute("BEGIN")
```

The yield statement only pauses the fixture.

Conceptually:

```text
BEGIN
    ↓
Transaction starts

yield
    ↓
Fixture pauses
```

These are completely different mechanisms.

| Feature  | Purpose                         |
| -------- | ------------------------------- |
| BEGIN    | Start tracking database changes |
| ROLLBACK | Discard tracked changes         |
| yield    | Pause fixture execution         |
| pytest   | Resume fixture later            |

---

## What Happens During a Test?

Example:

```python
def test_create_user(db_session):
    db_session.execute(
        "INSERT INTO users VALUES (1, 'Alice')"
    )
```

Timeline:

```text
BEGIN
    ↓
INSERT Alice
    ↓
ROLLBACK
```

Result:

```text
Alice does not exist after test completion.
```

---

## Why Does the Table Survive?

Consider our session fixture:

```python
conn.execute(
    "CREATE TABLE users (id INTEGER, name TEXT)"
)
```

This happens before any test transaction starts.

Timeline:

```text
CREATE TABLE users
    ↓
BEGIN
    ↓
INSERT Alice
    ↓
ROLLBACK
```

Result:

```text
users table exists
Alice row removed
```

The table survives because it was created before the transaction began.

The row disappears because it was created inside the transaction.

---

## Session Timeline in Our Example

```text
Pytest starts
    ↓
Create SQLite connection
    ↓
Create users table
    ↓
Test 1
    BEGIN
    INSERT Alice
    ROLLBACK
    ↓
Database clean again
    ↓
Test 2
    BEGIN
    INSERT Bob
    ROLLBACK
    ↓
Database clean again
    ↓
Pytest session ends
    ↓
conn.close()
```

This allows every test to start from a predictable database state.

---

## Why Use Transactions for Tests?

Without transactions:

```text
Test 1 inserts Alice
    ↓
Test 2 sees Alice
    ↓
Tests affect each other
```

This causes:

```text
Flaky tests
Unpredictable failures
Order-dependent behavior
```

With transactions:

```text
Test 1
    BEGIN
    INSERT Alice
    ROLLBACK

Test 2
    Starts clean
```

Every test gets isolation.

---

## Linux Analogy

Think of:

```text
Connection
```

as:

```text
Running container
```

And:

```text
Transaction
```

as:

```text
Temporary writable layer
```

Example:

```text
Container
    ↓
Make temporary changes
    ↓
Discard writable layer
```

The container still exists.

Only the temporary changes disappear.

Similarly:

```text
Connection remains alive
Transaction changes are discarded
```

after a rollback.

---

## Mental Model

Think of a transaction as a temporary workspace:

```text
Database
    ↓
BEGIN
    ↓
Temporary change workspace
    ↓
INSERT
UPDATE
DELETE
    ↓
ROLLBACK
    ↓
Workspace discarded
```

Or:

```text
Git repository
      ↓
Create temporary branch
      ↓
Make commits
      ↓
Delete branch
```

The main database remains unchanged.

---

## Common Misconceptions

### Misconception

```text
ROLLBACK closes the database connection.
```

Reality:

```text
ROLLBACK discards transaction changes.

Connection remains open.
```

---

### Misconception

```text
ROLLBACK deletes everything.
```

Reality:

```text
ROLLBACK removes only changes made after BEGIN.
```

---

### Misconception

```text
BEGIN creates a new database.
```

Reality:

```text
BEGIN starts a transaction on the existing connection.
```

---

### Misconception

```text
Transactions create namespaces.
```

Reality:

```text
Namespaces isolate visibility.

Transactions isolate changes.
```

---

### Misconception

```text
yield starts the transaction.
```

Reality:

```text
BEGIN starts the transaction.

yield only pauses fixture execution.
```

---

## Interview Questions

### Beginner

What is the purpose of BEGIN?

Expected Answer:

Start a transaction and begin tracking database changes.

---

### Beginner

What is the purpose of ROLLBACK?

Expected Answer:

Discard all changes made since BEGIN.

---

### Intermediate

Does ROLLBACK close the database connection?

Expected Answer:

No. It only discards transaction changes.

---

### Intermediate

Why does the `users` table survive a rollback in our example?

Expected Answer:

The table was created before the transaction started.

---

### Advanced

Why is transaction-based testing useful?

Expected Answer:

It provides test isolation while allowing tests to share the same database connection, making tests faster and more predictable.
