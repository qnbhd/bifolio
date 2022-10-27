import json
import logging
import os

import pika
from sanic import Blueprint
from sanic.response import redirect

from bifolio.domain.finance import get_holdings
from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit
from bifolio.domain.finance import get_stock_data
from bifolio.storage.storage import Storage
from bifolio.tools.jwt import inject_user_sec
from bifolio.tools.jwt import protected_sec


bp = Blueprint("profile", url_prefix="/profile")

log = logging.getLogger(__name__)


def send_to_rabbit(stocks_data_dict, host, port, queue):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
        )
    )

    body = json.dumps(stocks_data_dict).encode()

    queue = os.getenv("RABBITMQ_QUEUE", queue)
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )
    log.info(f"Stock data is sent to RabbitMQ")
    connection.close()


@bp.route("/", methods=["GET", "POST"])
@inject_user_sec()
@protected_sec(redirect_on_fail=True)
async def profile(request, user):
    """Profile endpoint."""

    if not user:
        return redirect(request.app.url_for("root"))

    # We need all the account info for the user so we can display it on the profile page
    storage: Storage = request.ctx.storage

    result = await storage.get_user_transactions(user["id"])

    txs = result.result

    if await request.app.ctx.redis.exists("BTC-USD"):
        btc_last_price = await request.app.ctx.redis.get("BTC-USD")
        btc_last_price = float(btc_last_price)
        log.info("Take BTC price from Redis")
    else:
        btc_last_price = get_stock_data("BTC-USD").iloc[-1]["Close"]

        log.info("Take BTC price from Yahoo Finance")

        send_to_rabbit(
            {"BTC-USD": float(btc_last_price)},
            host=request.app.config.RABBITMQ_HOST,
            port=request.app.config.RABBITMQ_PORT,
            queue=request.app.config.RABBITMQ_QUEUE,
        )

        log.info("Send BTC price to RabbitMQ")

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
