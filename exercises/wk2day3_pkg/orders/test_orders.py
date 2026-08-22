def test_override_wins(db):
    assert db["env"] == "orders_db"
    assert db["rows"] == ["seed"]

def test_parent_still_visible(base_url):
    assert base_url == "https://staging.internal"

def test_autouse_fired_for_everyone(audit_log):
    assert "test_autouse_fired_for_everyone" in audit_log