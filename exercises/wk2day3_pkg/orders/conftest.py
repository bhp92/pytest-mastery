import pytest

audit = []

@pytest.fixture
def db(db):
    db["env"] = "orders_db"
    db["rows"].append("seed")
    return db

@pytest.fixture(autouse=True)
def record_test(request):
    audit.append(request.node.name)

@pytest.fixture
def audit_log():
    return audit