def test_beta_sees_db(db):
    assert db["env"] == "root-db"