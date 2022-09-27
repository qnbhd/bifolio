import json

import plotly
from plotly import express as px
from plotly import graph_objs as go
from sanic import Blueprint
from sanic.response import redirect
from sanic_jwt import protected
from sqlalchemy import select

from bifolio.domain.finance import get_holdings
from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit
from bifolio.domain.finance import get_stock_data


bp = Blueprint("profile", url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@protected()
async def profile(request):
    """Profile endpoint."""
    if not request.ctx.session.get("loggedin"):
        return redirect("/account/login")

    from bifolio.database.models import Transaction
    from bifolio.database.models import User

    # We need all the account info for the user so we can display it on the profile page
    sess = request.ctx.db_session

    async with sess.begin():
        stmt = select(User).where(
            User.login == request.ctx.session["username"]
        )
        result = await sess.execute(stmt)
        row = result.one()
        account = row[0].__dict__

        stmt = select(Transaction).where(
            Transaction.user_id == account["id"]
        )
        result = await sess.execute(stmt)
        txs = result.scalars().all()

    df = get_portfolio_price(txs)
    btc_last_price = get_stock_data("BTC-USD").iloc[-1]["Close"]

    if not df.empty:
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
        fig = px.line(
            df, y="Close", color_discrete_sequence=["#d40606"]
        )
        fig.update_layout(template="plotly_white")
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
    else:
        fig = go.Figure()
        fig.update_layout(
            xaxis_rangeslider_visible=False, template="plotly_white"
        )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    price = get_portfolio_price(txs)

    if not price.empty:
        price = price.iloc[-1]["Close"]
        _, rel = get_portfolio_profit(txs)
    else:
        price, _, rel = 0, 0, 0

    # Show the profile page with account info
    return request.app.ctx.j2.render(
        "profile.html",
        request,
        account=account,
        btc_price=round(btc_last_price, 2),
        graphJSON=graphJSON,
        price=round(price, 2),
        profit_rel=round(rel, 2),
        holdings=get_holdings(txs),
    )
