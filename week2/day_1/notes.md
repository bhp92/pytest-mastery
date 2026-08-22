# 🧪 Week 2, Day 1 — Fixture Basics

### What it is / why it exists

A fixture is a function decorated with @pytest.fixture whose job is to supply something a test needs — data, an object, a connection, some prepared state. A test asks for it by putting the fixture's name in its parameter list, and pytest calls the fixture and passes the return value in. This is dependency injection.

Fixtures exist to kill the pain of xUnit-style setUp/tearDown. With setUp, every test in a class pays for setup whether it needs it or not, dependencies are implicit (you read the whole class to know what a test touches), and sharing setup across files means inheritance gymnastics. Fixtures fix all three: each test declares exactly what it needs by name, fixtures compose (a fixture can request other fixtures), and they can be shared without imports via conftest.py (Day 3). This explicit-dependencies property is the thing senior interviewers actually probe.

### Key concepts

@pytest.fixture turns a function into a fixture. By default its return value is what tests receive.
You request a fixture by naming it as a parameter — the parameter name must match the fixture name exactly. No import needed if it's in the same module (or a conftest.py on the path).

Fixtures compose: a fixture can take other fixtures as parameters, and pytest resolves the whole graph.

The default scope is function, so each test gets a fresh invocation (Day 2 covers wider scopes). This is what gives you test isolation.

request is a built-in fixture pytest injects on demand. It exposes the context of whoever asked: request.node (the test item, so request.node.name), request.config, request.module, request.param (Day 5), request.getfixturevalue(name), request.addfinalizer(...).

### Real-world production example

In a service test suite you almost never hand-build an authenticated client in each test. You write one fixture:

```python
@pytest.fixture
def api_client(base_config):
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {issue_test_token()}"
    session.base_url = f"https://{base_config['env']}.internal"
    return session
```

Every test that needs to hit the API just takes api_client as a parameter. Change auth once, the whole suite follows. The composition (api_client depends on base_config) is the everyday pattern.

### The 2 most common beginner mistakes

Calling the fixture like a function. Writing u = sample_user() inside a test instead of declaring sample_user as a parameter. Modern pytest rejects this outright (Fixtures are not meant to be called directly). A fixture is requested, never invoked by you.

Expecting a returned mutable object to carry state between tests. With the default function scope, each test triggers a fresh call to the fixture, so mutating the dict/list in one test does not show up in the next. Beginners get burned in both directions — surprised state doesn't persist, or surprised it "resets." (The name-match requirement is the close runner-up: a typo'd parameter gives fixture 'foo' not found.)

### Working example (verified passing on pytest 9.1.1)

```python
import pytest

# 1) Simplest fixture: a function that SUPPLIES a value.
@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Alice", "role": "admin"}


# 2) A test REQUESTS the fixture by naming it as a parameter.
#    pytest matches the name, calls the fixture, injects the return value.
def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"


# 3) Isolation: default (function) scope -> each test gets a fresh call,
#    so this mutation never leaks into the next test.
def test_user_role(sample_user):
    sample_user["role"] = "mutated"
    assert sample_user["role"] == "mutated"


def test_user_role_is_isolated(sample_user):
    assert sample_user["role"] == "admin"   # fresh, not "mutated"


# 4) Composition: a fixture can request other fixtures, exactly like a test.
@pytest.fixture
def admin_headers(sample_user):
    return {"Authorization": f"Bearer token-for-{sample_user['name']}"}


def test_headers_built_from_user(admin_headers):
    assert admin_headers["Authorization"] == "Bearer token-for-Alice"


# 5) The `request` object: built-in fixture exposing the requester's context.
@pytest.fixture
def labeled_payload(request):
    return {"data": [1, 2, 3], "requested_by": request.node.name}


def test_request_introspection(labeled_payload):
    assert labeled_payload["requested_by"] == "test_request_introspection"

```

I ran this — 5 passed. Try --setup-show on it to watch pytest build the fixture graph before each test; it makes the injection order concrete.