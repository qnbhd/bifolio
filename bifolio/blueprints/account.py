from sanic import Blueprint
from sanic.response import redirect


bp = Blueprint("account", url_prefix="/account")


@bp.route("/signup", methods=["GET", "POST"])
async def signup(request):
    """Sign up a new user endpoint."""

    return request.app.ctx.j2.render("register.html", request)


@bp.route("/logout")
def logout(request):
    """Logout endpoint."""

    # Remove session data, this will log the user out
    request.ctx.session.pop("loggedin", None)
    request.ctx.session.pop("id", None)
    request.ctx.session.pop("username", None)
    # Redirect to login page
    return redirect("/account/login")


@bp.route("/login", methods=["GET", "POST"])
async def login(request):
    """Login endpoint."""

    if request.ctx.session.get("loggedin"):
        return redirect("/home")
    return request.app.ctx.j2.render(
        "index.html", request, msg="Hello, world!"
    )
