from passlib.hash import bcrypt
from sanic_jwt import exceptions as jwte
from sanic_jwt import initialize
from sqlalchemy import select

from bifolio.database.models import User


def setup_auth(app):
    """Setup authentication.

    Args:
        app: Sanic application.
    """

    async def authenticate(request, *args, **kwargs):
        """Authenticate user."""

        login = request.json.get("username")
        password = request.json.get("password")

        sess = request.ctx.db_session

        async with sess.begin():
            stmt = select(User).where(User.login == login)
            result = await sess.execute(stmt)
            row = result.one()

        if not row:
            raise jwte.AuthenticationFailed("User not found")

        user = row[0]

        if not bcrypt.verify(password, user.password):
            raise jwte.AuthenticationFailed("Wrong password")

        request.ctx.session["loggedin"] = True
        request.ctx.session["username"] = user.login
        request.ctx.session["id"] = user.id

        return user.__dict__

    initialize(app, authenticate=authenticate, cookie_set=True)
