"""
============================================================================
Week 2 — Day 1 — Fixture Basics
============================================================================

HOW TO RUN
----------
Place this file at:  exercises/week2_day1.py

Run just this file (verbose):
    pytest exercises/week2_day1.py -v

Run and see fixture setup order / print output:
    pytest exercises/week2_day1.py -v -s

Show which fixtures a test resolves (great for debugging):
    pytest exercises/week2_day1.py --setup-show

SCOPE FOR TODAY
---------------
Only Day 1 concepts:
  - the @pytest.fixture decorator (a function that supplies data/state)
  - requesting a fixture by naming it as a test parameter (no import)
  - fixtures depending on other fixtures (composition)
  - the built-in `request` object

Do NOT use scope=, yield, params=, or conftest.py yet — those are Days 2–5.

Complete the tasks IN ORDER. Each builds on the previous one.
Write ONLY your own code. No solutions are provided.
============================================================================
"""

import pytest


# ---------------------------------------------------------------------------
# TASK 1 — Your first fixture
# ---------------------------------------------------------------------------
# a) Define a fixture named `base_config` that returns a dict:
#        {"env": "staging", "timeout": 30, "retries": 3}
# b) Write a test `test_config_env` that requests `base_config` as a
#    parameter and asserts env == "staging".
#
# Goal: prove you can supply data via a fixture and consume it by name.

@pytest.fixture
def base_config():
    return {"env": "staging", "timeout": 30, "retries": 3}

def test_config_env(base_config):
    assert base_config["env"] == "staging"

# ---------------------------------------------------------------------------
# TASK 2 — Reuse + isolation
# ---------------------------------------------------------------------------
# a) Write a second test `test_config_timeout` that requests the SAME
#    `base_config` fixture and asserts timeout == 30.
# b) In `test_config_timeout`, mutate the dict (e.g. set timeout = 999)
#    AFTER your assertion.
# c) Write a THIRD test `test_config_unchanged` that requests `base_config`
#    and asserts timeout is STILL 30 — proving each test gets a fresh value.
#
# Goal: understand default (function) scope gives each test its own object.

def test_config_timeout(base_config):
    assert base_config["timeout"] == 30
    base_config["timeout"] = 999

def test_config_unchanged(base_config):
    assert base_config["timeout"] == 30

# Question: Because default scope for fixture is test, are the mutation discarded after every test?
# If the scope was session, does the fixture carry mutation over to next tests?

# Yes. Default scope is function (you called it "test," same thing). Each test triggers a fresh call to the fixture, so the object is rebuilt and last test's mutation is gone. 
# With scope="session", the fixture runs once and every test receives the same object — so yes, mutations carry over and bleed between tests. 
# That's the exact "shared mutable state" trap Day 2 warns about. 
# One extra wrinkle for later: your CI runs -n auto (pytest-xdist, parallel), where "session" means per worker process, 
# not one global — so relying on session-scoped shared state is doubly fragile.

# ---------------------------------------------------------------------------
# TASK 3 — Fixtures depending on fixtures (composition)
# ---------------------------------------------------------------------------
# a) Define a fixture `api_client` that REQUESTS `base_config` and returns
#    a dict representing a fake client, e.g.:
#        {"base_url": f"https://{config['env']}.example.com",
#         "timeout": config["timeout"]}
# b) Write a test `test_client_url` that requests `api_client` (NOT
#    base_config directly) and asserts base_url == "https://staging.example.com".
#
# Goal: a fixture can consume another fixture the same way a test does.

@pytest.fixture
def api_client(base_config):
    return {
        "base_url": f"https://{base_config["env"]}.example.com",
        "timeout": base_config["timeout"]
    }

def test_client_url(api_client):
    assert api_client["base_url"] == "https://staging.example.com"

# Question: Here, does the base_config executes and injects the retrun value to api_client and then api_client to test_client_url?

# Yes, exactly. pytest builds the dependency graph first: base_config runs → its return value is injected into api_client → api_client runs → its return value is injected into test_client_url. 
# Run it with --setup-show and you'll literally see SETUP F base_config then SETUP F api_client stacked before the test. 
# Each fixture runs at most once per test regardless of how many things request it (pytest caches within scope).

# ---------------------------------------------------------------------------
# TASK 4 — The `request` object
# ---------------------------------------------------------------------------
# a) Define a fixture `tagged_record` that requests the built-in `request`
#    fixture and returns a dict:
#        {"payload": [1, 2, 3], "owner": <name of the requesting test>}
#    Hint: the requesting test's name is available on request.node.name
# b) Write a test `test_record_owner` that requests `tagged_record` and
#    asserts owner == "test_record_owner".
#
# Goal: read context that pytest injects about who is using the fixture.

@pytest.fixture
def tagged_record(request):
    return {
        "payload": [1, 2, 3],
        "owner": request.node.name
    }
def test_record_owner(tagged_record):
    assert tagged_record["owner"] == "test_record_owner"

# ---------------------------------------------------------------------------
# BONUS — Dynamic fixture lookup with request.getfixturevalue()
# ---------------------------------------------------------------------------
# Sometimes you don't know which fixture you need until the test decides.
#
# a) Keep your `base_config` and `api_client` fixtures from above.
# b) Define a fixture `resolver` that requests `request` and returns a
#    small function `_get(name)` which calls request.getfixturevalue(name)
#    and returns the result.
# c) Write a test `test_dynamic_resolution` that requests `resolver`,
#    then uses it to fetch "api_client" by string name at runtime, and
#    asserts its timeout == 30.
#
# Goal: understand that fixtures can be resolved lazily/by name — and think
#       about WHEN you'd want this vs. plain parameter injection (interview
#       favorite: the answer is "rarely; it hides dependencies").
# ---------------------------------------------------------------------------

@pytest.fixture
def resolver(request):
    def _get(name):
        return request.getfixturevalue(name)
    return _get


def test_dynamic_resolution(resolver):
    client = resolver("api_client")      # resolved by string, at call time
    assert client["timeout"] == 30

"""
Here's the mechanism. When you write def test_dynamic_resolution(resolver), pytest sees the parameter, calls the fixture function resolver for you, 
and binds the name resolver inside your test to whatever the fixture returned — which is _get. So inside the test, resolver is not the fixture anymore; it's the plain closure _get. 
The run above prints it:

injected object is: <function resolver.<locals>._get at 0x...>
is it the fixture?   _get

resolver.__name__ is '_get'. So resolver("api_client") is really _get("api_client"). You're calling the fixture's return value, not the fixture. 
The name collision (the parameter is spelled the same as the fixture) is what makes it look like you're calling the fixture, but the binding is to the injected object.

Contrast that with the thing that's actually forbidden:

python
def test_x():                 # base_config NOT requested as a parameter
    cfg = base_config()       # this name = the decorated fixture object

Here base_config was never requested, so the name still refers to the @pytest.fixture object itself. Calling it trips pytest's guard — the run shows the exact error:

Fixture "base_config" called directly. Fixtures are not meant to be called directly, but are created automatically when test functions request them as parameters.

(Small aside that honors precision: my demo's second test shows FAILED, not caught-by-pytest.raises. That's because pytest raises the direct-call error as an OutcomeException, 
which subclasses BaseException, not Exception — so a broad except Exception won't swallow it. The failure output is the proof the guard fired.)

So the corrected mental model:

Requesting a fixture = naming it as a parameter. pytest does the calling.
What you receive is the fixture's return/yield value.
If that value is data (a dict), you use it as data.
If that value is a function (a factory fixture), you call the function. That call is not "calling the fixture."
"""