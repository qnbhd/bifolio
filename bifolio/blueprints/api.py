import json as json_serializer

from passlib.hash import bcrypt
import plotly
from plotly import express as px
from sanic import Blueprint
from sanic import json
from sqlalchemy import select

from bifolio.database.models import Transaction
from bifolio.database.models import User
from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit


bp = Blueprint("api", url_prefix="/api")


@bp.route("/register", methods=["POST"])
async def create_user(request):
    """Create a new user endpoint."""

    login = request.json.get("username")
    password = bcrypt.hash(request.json.get("password"))

    conn = request.ctx.db_session

    async with request.ctx.db_session.begin():
        user = User(login=login, password=password)

    conn.add_all([user])
    await conn.commit()

    return json(user.login)


@bp.route("portfolio_js_plot", methods=["GET", "POST"])
async def portfolio_js_plot(request):
    """Get JSON plot data for portfolio."""

    if request.ctx.session.get("loggedin"):
        conn = request.ctx.db_session

        user_id = request.ctx.session.get("id")

        async with conn.begin():
            txs = await conn.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id
                )
            )
            txs = txs.scalars().all()

        df = get_portfolio_price(txs)

        fig = px.line(df, x="Date", y="Close")
        # candlestick = go.Candlestick(
        #     open=df["Open"],
        #     close=df["Close"],
        #     low=df["Low"],
        #     high=df["High"],
        # )
        # fig = go.Figure(data=[candlestick])
        # fig.update_layout(
        #     xaxis_rangeslider_visible=False, template="plotly_white"
        # )

        graphJSON = json_serializer.dumps(
            fig, cls=plotly.utils.PlotlyJSONEncoder
        )

        return json(graphJSON)


@bp.route("portfolio_profit", methods=["GET", "POST"])
async def portfolio_profit(request):
    """Get portfolio profit."""

    if request.ctx.session.get("loggedin"):
        conn = request.ctx.db_session

        user_id = request.ctx.session.get("id")

        async with conn.begin():
            txs = await conn.execute(
                select(Transaction).where(
                    Transaction.user_id == user_id
                )
            )
            txs = txs.scalars().all()

        result, rel = get_portfolio_profit(txs)
        return json(
            {"profit": round(result, 2), "rel": round(rel, 2)}
        )
