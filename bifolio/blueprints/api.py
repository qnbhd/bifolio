import json as json_serializer

from passlib.hash import bcrypt
import plotly
from plotly import express as px
from sanic import Blueprint
from sanic import json
from sanic_ext import validate
from sanic_jwt import inject_user
from sanic_jwt import protected

from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit
from bifolio.models import UserModel
from bifolio.storage.storage import Storage
from bifolio.tools.returns import Error


bp = Blueprint("api", url_prefix="/api")


@bp.route("/register", methods=["POST"])
@validate(json=UserModel, body_argument="person")
async def register(request, person: UserModel):
    """Create a new user endpoint."""

    login = person.username
    password = bcrypt.hash(person.password)

    storage = request.ctx.storage

    result = await storage.create_user(login, password)

    if isinstance(result, Error):
        return json(result.message, status=400)

    return json(result.result.__dict__, status=201)


@bp.route("portfolio_js_plot", methods=["GET", "POST"])
@inject_user()
@protected(redirect_on_fail=True)
async def portfolio_js_plot(request, user):
    """Get JSON plot data for portfolio."""

    # if request.ctx.session.get("loggedin"):
    storage: Storage = request.ctx.storage

    result = await storage.get_user_transactions(user.id)

    if isinstance(result, Error):
        return json(result.message, status=400)

    txs = result.result

    df = get_portfolio_price(txs)

    fig = px.line(df, x="Date", y="Close")

    graphJSON = json_serializer.dumps(
        fig, cls=plotly.utils.PlotlyJSONEncoder
    )

    return json(graphJSON)


@bp.route("portfolio_profit", methods=["GET", "POST"])
@inject_user()
@protected(redirect_on_fail=True)
async def portfolio_profit(request, user):
    """Get portfolio profit."""

    # if request.ctx.session.get("loggedin"):
    storage: Storage = request.ctx.storage

    result = await storage.get_user_transactions(user.id)

    if isinstance(result, Error):
        return json(result.message, status=400)

    txs = result.result

    result, rel = get_portfolio_profit(txs)
    return json({"profit": round(result, 2), "rel": round(rel, 2)})
