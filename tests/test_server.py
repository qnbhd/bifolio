async def test_fixture_test_client_get(app):
    """
    Simple index test.
    """

    request, response = await app.asgi_client.get("/account/login")
