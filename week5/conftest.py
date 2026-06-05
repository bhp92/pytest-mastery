"""
Week 5 conftest.py — Custom plugin hooks
This demonstrates how to add CLI options and filter tests based on them.
"""
import pytest


def pytest_addoption(parser):
    """Add a --slow flag to the pytest CLI."""
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Run tests marked as @pytest.mark.slow",
    )


def pytest_collection_modifyitems(config, items):
    """Skip @pytest.mark.slow tests unless --slow is passed."""
    if not config.getoption("--slow"):
        skip_slow = pytest.mark.skip(reason="Slow test — run with --slow to include")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_runtest_makereport(item, call):
    """
    Hook that fires after each test phase (setup / call / teardown).
    Here we attach the result to the item so fixtures can inspect it.
    """
    if call.when == "call":
        if call.excinfo is not None:
            # Test failed — you could log to a file, send a webhook, etc.
            pass
