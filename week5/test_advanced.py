"""
Week 5: Advanced Patterns
Run with: pytest week5/test_advanced.py -v
"""
import pytest
import asyncio


# ── Day 3: Async testing with pytest-asyncio ──────────────────────────────

async def fetch_data(url: str) -> dict:
    """Simulates an async HTTP fetch."""
    await asyncio.sleep(0.01)
    return {"url": url, "status": 200}


async def fetch_multiple(urls: list) -> list:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("https://api.example.com/users")
    assert result["status"] == 200
    assert "url" in result


@pytest.mark.asyncio
async def test_fetch_multiple():
    urls = ["https://api.example.com/a", "https://api.example.com/b"]
    results = await fetch_multiple(urls)
    assert len(results) == 2
    assert all(r["status"] == 200 for r in results)


@pytest.mark.asyncio
async def test_async_mock(mocker):
    """Mock an async function using AsyncMock."""
    mock_fetch = mocker.AsyncMock(return_value={"status": 200, "data": "mocked"})
    mocker.patch("week5.test_advanced.fetch_data", mock_fetch)

    result = await fetch_data("https://anything.com")
    assert result["data"] == "mocked"
    mock_fetch.assert_awaited_once()


# ── Async fixture ──────────────────────────────────────────────────────────

@pytest.fixture
async def async_client():
    """Async fixture — works with asyncio_mode=auto in pytest.ini."""
    client = {"connected": True, "calls": 0}
    yield client
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    assert async_client["connected"] is True


# ── Day 4: Custom conftest hooks ──────────────────────────────────────────
# (See week5/conftest.py for pytest_addoption and pytest_collection_modifyitems)

@pytest.mark.slow
def test_marked_slow():
    """Only runs with pytest --slow (controlled by week5/conftest.py)."""
    assert True


# ── Day 5: Fixture factory with cleanup ────────────────────────────────────

@pytest.fixture
def registry():
    """A fixture that returns a factory + tracks everything for teardown."""
    items = {}

    def register(key, value):
        items[key] = value
        return value

    yield register

    # Teardown: clear everything registered
    items.clear()


def test_registry_stores_item(registry):
    obj = registry("service_a", {"name": "Auth"})
    assert obj["name"] == "Auth"


def test_registry_multiple(registry):
    registry("a", 1)
    registry("b", 2)
    # Each test gets a fresh registry — factory pattern ensures isolation


# ── Day 2: Coverage markers ────────────────────────────────────────────────

def complex_function(x: int, flag: bool) -> str:
    """This function has multiple branches — good for branch coverage practice."""
    if x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    elif flag:
        return "positive-flagged"
    else:
        return "positive"


@pytest.mark.parametrize("x, flag, expected", [
    (-1, False, "negative"),
    (0,  False, "zero"),
    (5,  True,  "positive-flagged"),
    (5,  False, "positive"),
])
def test_all_branches(x, flag, expected):
    """
    These 4 cases give 100% branch coverage of complex_function.
    Run: pytest week5/ --cov=week5 --cov-branch --cov-report=term-missing
    """
    assert complex_function(x, flag) == expected
