from passlib.hash import bcrypt
from sanic_jwt import exceptions as jwte
from sanic_jwt import initialize

from bifolio.storage.storage import Storage
from bifolio.tools.returns import Error


def setup_auth(app):
    """Setup authentication.

    Args:
        app: Sanic application.
    """

    from sanic_jwt import Claim

    class MyCustomClaim(Claim):
        key = "user_id"

        def setup(self, payload, user):
            return user["id"]

        def verify(self, value):
            return True

    async def authenticate(request, *args, **kwargs):
        """Authenticate user."""

        login = request.json.get("username")
        password = request.json.get("password")

        storage: Storage = request.ctx.storage

        result = await storage.get_user(login, method="login")

        if isinstance(result, Error):
            raise jwte.AuthenticationFailed(result.message)

        user = result.result

        if not bcrypt.verify(password, user.password):
            raise jwte.AuthenticationFailed("Wrong password")

        return user.__dict__

    async def retrieve_user(request, payload, *args, **kwargs):
        if not payload:
            return None

        user_id = payload.get("user_id", None)

        result = await request.ctx.storage.get_user(user_id)

        if isinstance(result, Error):
            return None

        return result.result.__dict__

    async def store_refresh_token(
        user_id: str, refresh_token: str, request
    ) -> None:
        """The actual keyword argument being passed is `user_id`, but the
        value that it is retrieving is the eid"""
        key = f"refresh_token:{user_id}"
        redis = request.app.ctx.redis
        await redis.set(key, refresh_token)

    async def retrieve_refresh_token(request, user_id: str) -> str:
        key = f"refresh_token:{user_id}"
        redis = request.app.ctx.redis
        return await redis.get(key)

    initialize(
        app,
        authenticate=authenticate,
        custom_claims=[MyCustomClaim],
        retrieve_user=retrieve_user,
        store_refresh_token=store_refresh_token,
        retrieve_refresh_token=retrieve_refresh_token,
        cookie_set=True,
    )
