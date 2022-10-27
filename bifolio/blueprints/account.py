from contextlib import suppress

from sanic import Blueprint
from sanic.response import redirect
from sanic_jwt import inject_user

from bifolio.tools.jwt import inject_user_sec


bp = Blueprint("account", url_prefix="/account")


@bp.route("/signup", methods=["GET", "POST"])
@inject_user_sec()
async def signup(request, user):
    """Sign up a new user endpoint."""

    if user:
        return redirect(request.app.url_for("home.home"))

    return request.app.ctx.j2.render("register.html", request)


@bp.route("/logout")
@inject_user_sec()
async def logout(request, user):
    """Logout endpoint."""

    if not user:
        return redirect(request.app.url_for("root"))

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
@inject_user_sec()
async def login(request, user):
    """Login endpoint."""

    if user:
        return redirect(request.app.url_for("home.home"))

    return request.app.ctx.j2.render(
        "login.html", request, msg="Hello, world!"
    )
