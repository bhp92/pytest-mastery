"""
============================================================================
Week 2 — Day 3 — conftest.py Patterns
============================================================================

HOW TO RUN
----------
Place this file at:  exercises/week2_day3.py

Today's topic lives across DIRECTORIES, not one flat file. You'll build a
tiny package next to this file and run pytest against it. Create this tree:

    exercises/
    ├── week2_day3.py              <- THIS file (instructions + Task 1 tests)
    └── wk2day3_pkg/
        ├── conftest.py            <- Task 1 & 2 (root fixtures for the pkg)
        ├── test_alpha.py          <- Task 1
        ├── test_beta.py           <- Task 2
        └── orders/
            ├── conftest.py        <- Task 3 (override) + Task 4 (autouse)
            └── test_orders.py     <- Task 3 & 4

Run just today's package (verbose):
    pytest exercises/wk2day3_pkg/ -v

SEE which conftest a fixture resolves to (today's single best flag):
    pytest exercises/wk2day3_pkg/orders/test_orders.py --fixtures | head -40

WATCH setup/teardown so you can see autouse fire on every test:
    pytest exercises/wk2day3_pkg/ -v -s --setup-show

Prove order-independence once you're done (Task 4 depends on it):
    pytest exercises/wk2day3_pkg/ -p randomly -v      # if pytest-randomly installed

SCOPE FOR TODAY
---------------
Only Day 3 concepts:
  - conftest.py is auto-DISCOVERED up the directory tree — NEVER imported
  - a conftest fixture is shared by every test at/below its directory, no import
  - most-LOCAL fixture wins when names clash (override in a child directory)
  - non-overridden names still resolve UPWARD to a parent conftest
  - autouse fixtures in conftest.py run for every test in the subtree

Keep it to conftest patterns. You already know fixtures (Day 1) and scopes
(Day 2); use them, but today is about WHERE a fixture lives and how pytest
finds it. You do NOT need yield-teardown depth (that's Day 4) or params
(that's Day 5).

RULE THAT WILL BITE YOU: never write `from conftest import ...`. If you type
the word `import` for a fixture today, you've taken a wrong turn.

Complete the tasks IN ORDER. Each builds on the previous one.
Write ONLY your own code. No solutions are provided.
============================================================================
"""

# ---------------------------------------------------------------------------
# TASK 1 — Auto-discovery: a conftest fixture reaches a test with NO import
# ---------------------------------------------------------------------------
# a) Create the folder  exercises/wk2day3_pkg/  with an (empty) conftest.py
#    and an (empty) __init__.py is NOT required — leave it out.
# b) In  wk2day3_pkg/conftest.py  define a fixture `base_url` that returns
#    the string  "https://staging.internal".
# c) In  wk2day3_pkg/test_alpha.py  write `test_alpha_sees_base_url` that
#    requests `base_url` (as a parameter — no import!) and asserts it equals
#    "https://staging.internal".
#
# Goal: prove pytest injects a conftest fixture by NAME, with no import,
#       purely because the test lives at/below that conftest's directory.


# ---------------------------------------------------------------------------
# TASK 2 — Sharing across files: a SECOND test file, same fixture, no import
# ---------------------------------------------------------------------------
# a) In  wk2day3_pkg/conftest.py  add a second fixture `db` that returns
#    {"env": "root-db", "rows": []}.
# b) In a NEW file  wk2day3_pkg/test_beta.py  write `test_beta_sees_db`
#    that requests `db` and asserts db["env"] == "root-db".
# c) test_alpha.py and test_beta.py are different files. Neither imports the
#    other and neither imports conftest. In a comment, answer: what single
#    property of conftest.py makes the SAME `db` fixture usable from both
#    files without any import or duplication?
#
# Goal: feel the actual payoff of conftest — share one fixture across many
#       test files with zero import coupling.

# Answer: Pytest Autodiscovery makes the conftest.py fixtures injectable by name to any test function in scope.

# ---------------------------------------------------------------------------
# TASK 3 — Override in a child directory: the most-LOCAL fixture wins
# ---------------------------------------------------------------------------
# a) Create a subdirectory  wk2day3_pkg/orders/  with its own conftest.py.
# b) In  wk2day3_pkg/orders/conftest.py  define a fixture named `db`
#    (SAME name as the parent) that returns {"env": "orders-db", "rows": []}.
# c) In  wk2day3_pkg/orders/test_orders.py  write:
#       - test_override_wins : requests `db`, asserts db["env"]=="orders-db"
#       - test_parent_still_visible : requests `base_url` (which orders/ does
#         NOT define) and asserts it == "https://staging.internal"
# d) In a comment, state the two rules you just proved:
#       (i)  when two conftests define the same name, which one wins?
#       (ii) when a name is NOT overridden locally, where does it resolve?
#
# Goal: prove override-by-location — a child conftest shadows a parent
#       fixture of the same name for its subtree only, while unrelated
#       parent fixtures keep resolving upward.

# Answer (i): Most local conftest wins
# Answer (ii): If not found locally, autodiscovery walks upwards and finds in parent conftest.py 

# ---------------------------------------------------------------------------
# TASK 4 — autouse in conftest.py: runs for EVERY test in the subtree
# ---------------------------------------------------------------------------
# This mirrors the real pattern in your repo's week2/conftest.py
# (the `clean_users_table` autouse fixture). Build the same idea.
#
# a) In  wk2day3_pkg/orders/conftest.py  add a module-level list at the top:
#       audit = []
# b) Add an autouse fixture `record_test` (use @pytest.fixture(autouse=True))
#    that appends request.node.name to `audit` on setup. It takes `request`.
#    No test will REQUEST this fixture — it must run anyway.
# c) In test_orders.py add `test_autouse_fired_for_everyone` that imports
#    `audit` from orders.conftest?  NO — you must NOT import conftest.
#    Instead: request the fixture value indirectly. Add a small NON-autouse
#    fixture `audit_log` in orders/conftest.py that simply returns `audit`,
#    then have the test request `audit_log` and assert that its OWN name is
#    already in the list (autouse ran before the test body).
# d) In a comment, answer: give one real production job an autouse conftest
#    fixture does that you would NOT want to repeat in every test signature.
#
# Goal: prove an autouse fixture in a conftest applies to an entire subtree
#       automatically, and connect it to the cleanup pattern in your repo.

# Answer: The reason autouse-in-conftest exists is cross-cutting per-test 
# work that has nothing to do with what any individual test asserts. 
# The tell is: "every test in this subtree needs X to happen, but no test 
# should have to ask for X." Real jobs:

# State reset / transaction rollback — wrap each test in a DB transaction and 
# roll it back on teardown (your repo's clean_users_table is the lite version). 
# This is the big one.
#
# Time control — freeze the clock so time-dependent assertions are deterministic.
#
# Environment isolation — set/clear env vars, or install a "no real network" guard 
# so a stray requests.get fails loudly instead of hitting prod.
#
# Cache/singleton reset — clear an app-level cache or reset a module singleton between tests.

# ---------------------------------------------------------------------------
# BONUS — Override that EXTENDS the parent (same-name request, no recursion)
# ---------------------------------------------------------------------------
# The override in Task 3 REPLACED the parent `db` entirely. Sometimes you
# want the child to build ON TOP of the parent's value instead.
#
# a) Change  wk2day3_pkg/orders/conftest.py  so its `db` fixture takes a
#    parameter also named `db`:
#
#        @pytest.fixture
#        def db(db):                     # <- same name as the parent
#            db["env"] = "orders-db"     # start from the PARENT dict
#            db["rows"].append("seed")   # then extend it
#            return db
#
# b) Update test_override_wins to also assert db["rows"] == ["seed"], proving
#    the child received the PARENT's object and modified it (not a fresh one).
# c) Run it. It does NOT infinitely recurse. In a comment, explain WHY:
#    when an override names its own fixture as a parameter, which fixture
#    does pytest resolve that parameter to — the override itself, or the
#    next one up the tree? State the rule in one line.
#
# When a fixture overrides another of the same name and requests that name, 
# pytest binds the parameter to the next definition up the tree, not to the 
# fixture itself — so the chain resolves parent → child exactly once and terminates.
#
# Goal: know the extend-vs-replace override technique cold. "How do you make
#       a child conftest fixture build on the parent of the same name without
#       recursing?" is a sharp senior probe — the answer is this exact rule.
# ---------------------------------------------------------------------------