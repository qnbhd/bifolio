def test_fixture_test_client_get(app):
    """
    Simple index test.
    """

    req, resp = app.test_client.get("/")
    assert resp.status == 200
    assert resp.json == {"hello": "world"}
