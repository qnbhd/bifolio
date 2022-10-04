from sanic import Blueprint
from sanic_jwt import inject_user

from bifolio.domain.finance import get_holdings
from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit
from bifolio.domain.finance import get_stock_data
from bifolio.storage.storage import Storage
from bifolio.tools.jwt import protected_sec


bp = Blueprint("profile", url_prefix="/profile")


@bp.route("/", methods=["GET", "POST"])
@inject_user()
@protected_sec(redirect_on_fail=True)
async def profile(request, user):
    """Profile endpoint."""

    # We need all the account info for the user so we can display it on the profile page
    storage: Storage = request.ctx.storage

    result = await storage.get_user_transactions(user["id"])

    txs = result.result

    btc_last_price = get_stock_data("BTC-USD").iloc[-1]["Close"]

    if txs:
        df = get_portfolio_price(txs)

        price = df.iloc[-1]["Close"]
        _, rel = get_portfolio_profit(txs)

        chart_data = df["Close"].to_list()
        chart_dates = df.index.astype(str).to_list()
    else:
        price, _, rel = 0, 0, 0
        chart_data = []
        chart_dates = []

    # Show the profile page with account info
    return request.app.ctx.j2.render(
        "profile.html",
        request,
        account=user,
        btc_price=round(btc_last_price, 2),
        price=round(price, 2),
        profit_rel=round(rel, 2),
        holdings=get_holdings(txs),
        chart_data=chart_data,
        chart_dates=chart_dates,
    )
