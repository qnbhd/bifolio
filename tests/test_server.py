import pytest
import requests
from sqlalchemy import select

from bifolio import __static_src_folder__
from bifolio.database.models import User


async def make_register_request(app, username, password):
    """
    Make one register request.
    """

    request, response = await app.asgi_client.post(
        app.url_for("api.register"),
        json={
            "username": username,
            "password": password,
        },
    )

    return request, response


async def make_login_request(app, username, password):
    """
    Make login request.
    """

    request, response = await app.asgi_client.post(
        "/auth",
        json={
            "username": username,
            "password": password,
        },
    )

    return request, response


async def make_profile_request(app, access_token):
    """
    Make profile request.
    """

    request, response = await app.asgi_client.get(
        app.url_for("profile.profile"),
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    return request, response


@pytest.mark.parametrize(
    "username,password,expected_code",
    [
        ("test", "test", 400),
        ("", "", 400),
        ("username", "password", 201),
    ],
)
async def test_signup(app, username, password, expected_code):
    """
    Test register.
    """

    request, response = await make_register_request(
        app, username, password
    )

    assert response.status == expected_code

    if not expected_code == 200:
        return

    conn = request.ctx.db_session

    async with conn.begin():
        users = await conn.execute(select(User))
        users = users.scalars().all()

    assert len(users) == 1


async def test_login(app):
    """
    Test register and login.
    """

    await make_register_request(app, "test_12345", "test_12345")

    request, response = await make_login_request(
        app, "test_12345", "test_12345"
    )

    assert response.status == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


async def test_authorize(app):
    """
    Test register and login.
    """

    await make_register_request(app, "test_12345", "test_12345")

    request, response = await make_login_request(
        app, "test_12345", "test_12345"
    )
    access_token = response.json["access_token"]

    request, response = await make_profile_request(app, access_token)

    assert response.status == 200

    with open(__static_src_folder__ / "profile.html") as f:
        content = f.read()

    assert len(response.text) > len(content)


async def test_logout(app):
    """
    Test logout.
    """

    await make_register_request(app, "test_12345", "test_12345")

    request, response = await make_login_request(
        app, "test_12345", "test_12345"
    )
    access_token = response.json["access_token"]

    request, response = await make_profile_request(app, access_token)
    assert response.status == 200

    request, response = await app.asgi_client.get(
        app.url_for("account.logout"),
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status == requests.codes.found

    request, response = await make_profile_request(app, access_token)

    assert response.status == 302
