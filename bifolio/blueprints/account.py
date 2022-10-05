from contextlib import suppress

from sanic import Blueprint
from sanic.response import redirect
from sanic_jwt import inject_user


bp = Blueprint("account", url_prefix="/account")


@bp.route("/signup", methods=["GET", "POST"])
async def signup(request):
    """Sign up a new user endpoint."""

    return request.app.ctx.j2.render("register.html", request)


@bp.route("/logout")
@inject_user()
async def logout(request, user):
    """Logout endpoint."""

    # Remove session data, this will log the user out
    token = request.cookies.pop("access_token")
    request.cookies.pop("refresh_token")

    await request.app.ctx.redis.set(
        f"blacklist:{token}", "true", ex=60 * 60 * 24
    )
    with suppress(AttributeError):
        await request.app.ctx.redis.delete(f"refresh_token:{user.id}")

    return redirect("/profile")


@bp.route("/login", methods=["GET", "POST"])
async def login(request):
    """Login endpoint."""

    return request.app.ctx.j2.render(
        "index.html", request, msg="Hello, world!"
    )
