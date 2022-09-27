from sanic import Blueprint
from sanic.response import redirect


bp = Blueprint("home", url_prefix="/home")


@bp.route("/", methods=["GET", "POST"])
async def home(request):
    """Home endpoint."""

    if request.ctx.session.get("loggedin"):
        return request.app.ctx.j2.render("home.html", request)

    return redirect("/account/login")
