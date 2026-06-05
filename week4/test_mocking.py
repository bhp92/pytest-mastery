"""
Week 4: Mocking & Patching
Run with: pytest week4/test_mocking.py -v
"""
import pytest
import requests


# ── The code we're testing (normally this would be in src/) ───────────────

class UserService:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id: int) -> dict:
        response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def get_user_name(self, user_id: int) -> str:
        user = self.get_user(user_id)
        return user["name"]


class EmailSender:
    def send(self, to: str, subject: str, body: str) -> bool:
        # Pretend this calls an external SMTP server
        raise NotImplementedError("Don't call this in tests!")


class NotificationService:
    def __init__(self, email_sender: EmailSender):
        self.sender = email_sender

    def notify_user(self, email: str, message: str) -> bool:
        return self.sender.send(
            to=email,
            subject="Notification",
            body=message,
        )


# ── Day 1: unittest.mock basics ───────────────────────────────────────────

from unittest.mock import MagicMock, patch

def test_mock_return_value():
    mock_func = MagicMock(return_value=42)
    assert mock_func() == 42
    assert mock_func.call_count == 1


def test_mock_side_effect():
    mock_func = MagicMock(side_effect=[1, 2, ValueError("boom")])
    assert mock_func() == 1
    assert mock_func() == 2
    with pytest.raises(ValueError, match="boom"):
        mock_func()


# ── Day 2: pytest-mock (mocker fixture) ───────────────────────────────────

def test_get_user_mocked(mocker):
    """Patch requests.get so we never hit the real API."""
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "Leanne Graham"}
    mock_response.raise_for_status.return_value = None

    mocker.patch("requests.get", return_value=mock_response)

    service = UserService()
    user = service.get_user(1)

    assert user["name"] == "Leanne Graham"
    requests.get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/users/1"
    )


def test_get_user_name(mocker):
    """Patch at a higher level — mock the whole get_user method."""
    service = UserService()
    mocker.patch.object(service, "get_user", return_value={"id": 1, "name": "Alice"})

    name = service.get_user_name(1)
    assert name == "Alice"


def test_email_sender_called(mocker):
    """Use mocker.MagicMock() to inject a fake dependency."""
    fake_sender = mocker.MagicMock(spec=EmailSender)
    fake_sender.send.return_value = True

    svc = NotificationService(email_sender=fake_sender)
    result = svc.notify_user("alice@example.com", "Hello!")

    assert result is True
    fake_sender.send.assert_called_once_with(
        to="alice@example.com",
        subject="Notification",
        body="Hello!",
    )


# ── Day 3: monkeypatch ────────────────────────────────────────────────────

import os

def get_api_key():
    key = os.environ.get("API_KEY")
    if not key:
        raise EnvironmentError("API_KEY not set")
    return key


def test_env_var_with_monkeypatch(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-secret-123")
    assert get_api_key() == "test-secret-123"


def test_env_var_missing(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(EnvironmentError, match="API_KEY not set"):
        get_api_key()


CONFIG = {"timeout": 30, "retries": 3}

def test_monkeypatch_dict(monkeypatch):
    monkeypatch.setitem(CONFIG, "timeout", 5)
    assert CONFIG["timeout"] == 5
    # After the test, CONFIG["timeout"] is restored to 30 automatically


# ── Day 2: mocker.spy ─────────────────────────────────────────────────────

def test_spy_on_method(mocker):
    """spy wraps the real method — it still runs, but you can assert on calls."""
    service = UserService()
    spy = mocker.spy(service, "get_user_name")

    # We still need to mock the HTTP call
    mock_resp = mocker.MagicMock()
    mock_resp.json.return_value = {"id": 1, "name": "Alice"}
    mock_resp.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_resp)

    service.get_user_name(1)
    spy.assert_called_once_with(1)


# ── Day 4: patch as context manager ──────────────────────────────────────

def test_patch_context_manager():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 99}
        mock_get.return_value.raise_for_status.return_value = None

        service = UserService()
        user = service.get_user(99)
        assert user["id"] == 99
