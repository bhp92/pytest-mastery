"""
Exercises — Try each one before reading the solution!

Instructions:
1. Read the problem statement
2. Write your solution in the EXERCISE block
3. Run: pytest exercises/test_exercises.py -v
4. Stuck? Uncomment the SOLUTION block to compare

Run exercises only:    pytest exercises/ -v
Run with solutions:    pytest exercises/ -v --tb=short
"""
import pytest
import json
import os
from unittest.mock import MagicMock


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 1 — Beginner: Parametrize
# ════════════════════════════════════════════════════════════════════════════
# Problem: The function below classifies a BMI value.
# Write a single parametrized test that covers all 4 categories.

def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    elif bmi < 25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else:
        return "obese"


# ── YOUR SOLUTION ────────────────────────────────────────────────────────────
# @pytest.mark.parametrize("bmi, expected", [
#     ...fill in...
# ])
# def test_classify_bmi(bmi, expected):
#     ...


# ── REFERENCE SOLUTION (delete/comment once you've tried) ───────────────────
@pytest.mark.parametrize("bmi, expected", [
    (15.0, "underweight"),
    (22.0, "normal"),
    (27.5, "overweight"),
    (35.0, "obese"),
    (18.5, "normal"),     # boundary: exactly 18.5 → normal
    (24.99, "normal"),    # boundary: just under 25 → normal
])
def test_classify_bmi(bmi, expected):
    assert classify_bmi(bmi) == expected


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 2 — Beginner: pytest.raises
# ════════════════════════════════════════════════════════════════════════════
# Problem: Write tests that verify parse_age raises the right exceptions
# with the right messages.

def parse_age(value: str) -> int:
    try:
        age = int(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid integer")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is out of range (0-150)")
    return age


# ── YOUR SOLUTION ────────────────────────────────────────────────────────────
# def test_parse_age_valid():   ...
# def test_parse_age_not_int(): ...
# def test_parse_age_negative(): ...


# ── REFERENCE SOLUTION ───────────────────────────────────────────────────────
def test_parse_age_valid():
    assert parse_age("25") == 25
    assert parse_age("0") == 0
    assert parse_age("150") == 150


def test_parse_age_not_integer():
    with pytest.raises(ValueError, match="not a valid integer"):
        parse_age("abc")


def test_parse_age_out_of_range():
    with pytest.raises(ValueError, match="out of range"):
        parse_age("-1")
    with pytest.raises(ValueError, match="out of range"):
        parse_age("151")


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 3 — Intermediate: Fixtures with yield (setup/teardown)
# ════════════════════════════════════════════════════════════════════════════
# Problem: Create a fixture that:
# - Creates a temp JSON config file before the test
# - Yields the file path
# - Deletes the file after the test (even if the test fails)

def load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


# ── YOUR SOLUTION ────────────────────────────────────────────────────────────
# @pytest.fixture
# def config_file(tmp_path):
#     ...


# ── REFERENCE SOLUTION ───────────────────────────────────────────────────────
@pytest.fixture
def config_file(tmp_path):
    path = tmp_path / "config.json"
    data = {"debug": True, "max_retries": 3, "timeout": 30}
    path.write_text(json.dumps(data))
    yield str(path)
    # teardown — tmp_path auto-cleans, but explicit is clearer:
    if path.exists():
        path.unlink()


def test_load_config(config_file):
    config = load_config(config_file)
    assert config["debug"] is True
    assert config["max_retries"] == 3


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 4 — Intermediate: Mocking an external service
# ════════════════════════════════════════════════════════════════════════════
# Problem: OrderProcessor.process() calls PaymentGateway.charge().
# Write a test that:
# - Mocks the payment gateway so no real charge happens
# - Verifies charge() was called with the correct amount
# - Tests the failure path when charge() raises an exception

class PaymentGateway:
    def charge(self, amount: float, card_token: str) -> dict:
        raise NotImplementedError("Never call this in tests!")


class InsufficientFundsError(Exception):
    pass


class OrderProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process(self, amount: float, card_token: str) -> str:
        try:
            result = self.gateway.charge(amount, card_token)
            return f"Order processed: {result.get('transaction_id')}"
        except InsufficientFundsError:
            return "Payment declined: insufficient funds"


# ── YOUR SOLUTION ────────────────────────────────────────────────────────────
# def test_successful_payment(mocker): ...
# def test_declined_payment(mocker): ...


# ── REFERENCE SOLUTION ───────────────────────────────────────────────────────
def test_successful_payment(mocker):
    fake_gateway = mocker.MagicMock(spec=PaymentGateway)
    fake_gateway.charge.return_value = {"transaction_id": "txn_abc123"}

    processor = OrderProcessor(gateway=fake_gateway)
    result = processor.process(99.99, "card_tok_xyz")

    assert result == "Order processed: txn_abc123"
    fake_gateway.charge.assert_called_once_with(99.99, "card_tok_xyz")


def test_declined_payment(mocker):
    fake_gateway = mocker.MagicMock(spec=PaymentGateway)
    fake_gateway.charge.side_effect = InsufficientFundsError("Card declined")

    processor = OrderProcessor(gateway=fake_gateway)
    result = processor.process(500.0, "card_tok_xyz")

    assert result == "Payment declined: insufficient funds"


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 5 — Advanced: Fixture factory + indirect parametrize
# ════════════════════════════════════════════════════════════════════════════
# Problem: Create a fixture factory that builds API clients with different
# auth levels. Use indirect parametrize to test each level.

class APIClient:
    def __init__(self, auth_level: str):
        self.auth_level = auth_level
        self._endpoints = {
            "public":    ["/health", "/status"],
            "user":      ["/health", "/status", "/profile", "/data"],
            "admin":     ["/health", "/status", "/profile", "/data", "/admin"],
        }

    def can_access(self, endpoint: str) -> bool:
        return endpoint in self._endpoints.get(self.auth_level, [])


# ── YOUR SOLUTION ────────────────────────────────────────────────────────────
# @pytest.fixture
# def api_client(request): ...
#
# @pytest.mark.parametrize("api_client, endpoint, expected", [...], indirect=["api_client"])
# def test_endpoint_access(api_client, endpoint, expected): ...


# ── REFERENCE SOLUTION ───────────────────────────────────────────────────────
@pytest.fixture
def api_client(request):
    return APIClient(auth_level=request.param)


@pytest.mark.parametrize("api_client, endpoint, expected", [
    ("public", "/health",  True),
    ("public", "/profile", False),
    ("user",   "/profile", True),
    ("user",   "/admin",   False),
    ("admin",  "/admin",   True),
    ("admin",  "/health",  True),
], indirect=["api_client"])
def test_endpoint_access(api_client, endpoint, expected):
    assert api_client.can_access(endpoint) == expected


# ════════════════════════════════════════════════════════════════════════════
# EXERCISE 6 — Advanced: Custom conftest hook
# ════════════════════════════════════════════════════════════════════════════
# Problem: See exercises/conftest.py — it implements a --env flag.
# These tests use it to check environment-specific behavior.

def get_base_url(env: str) -> str:
    urls = {
        "dev":  "http://localhost:8000",
        "staging": "https://staging.api.example.com",
        "prod": "https://api.example.com",
    }
    return urls.get(env, urls["dev"])


def test_dev_url():
    assert get_base_url("dev") == "http://localhost:8000"


def test_staging_url():
    assert get_base_url("staging") == "https://staging.api.example.com"


def test_default_is_dev():
    assert get_base_url("unknown") == "http://localhost:8000"
