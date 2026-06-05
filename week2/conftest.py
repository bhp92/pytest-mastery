"""
Week 2 conftest.py
Fixtures here are available to ALL tests in week2/ without any import.
"""
import pytest
import sqlite3


@pytest.fixture(scope="session")
def db_connection():
    """
    Session-scoped: one DB connection for the entire test session.
    Teardown runs after ALL tests finish.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def clean_users_table(db_connection):
    """
    autouse=True: runs for EVERY test in week2/ automatically.
    Rolls back user data after each test so tests don't bleed into each other.
    """
    yield
    db_connection.execute("DELETE FROM users")
    db_connection.commit()
