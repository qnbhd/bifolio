from datetime import datetime

from sanic import Blueprint
from sanic import json


bp = Blueprint("transactions", url_prefix="/transactions")


@bp.route("/make", methods=["GET", "POST"])
async def make_transaction(request):
    """Make a transaction endpoint."""

    from bifolio.database.models import Transaction

    if request.ctx.session.get("loggedin"):
        conn = request.ctx.db_session

        date = datetime.strptime(
            f'{request.json.get("tx_date")}'
            f' {request.json.get("tx_time")}',
            "%d/%m/%Y %H:%M",
        )

        print(request.json)

        async with conn.begin():
            tx = Transaction(
                user_id=request.ctx.session.get("id"),
                kind=request.json.get("action"),
                amount=request.json.get("amount"),
                coin=request.json.get("currency"),
                price=request.json.get("price"),
                date=date,
            )

        conn.add_all([tx])
        await conn.commit()

        return json({})
