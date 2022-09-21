def test_fixture_test_client_get(app):
    """
    Simple index test.
    """

    req, resp = app.test_client.get("/hello")
    assert resp.text == "Hello, world!"
