import pytest

@pytest.fixture
def base_url():
    return "https://staging.internal"

@pytest.fixture
def db():
    return {"env": "root-db", "rows": []}