from sanic import Blueprint
from sanic_jwt import protected


bp = Blueprint("home", url_prefix="/home")


@bp.route("/", methods=["GET", "POST"])
@protected(redirect_on_fail=True)
async def home(request):
    """Home endpoint."""

    return request.app.ctx.j2.render("home.html", request)
