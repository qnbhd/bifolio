from datetime import datetime

from sanic import Blueprint
from sanic import json
from sanic_jwt import inject_user

from bifolio.tools.jwt import protected_sec
from bifolio.tools.returns import Error


bp = Blueprint("transactions", url_prefix="/transactions")


@bp.route("/make", methods=["GET", "POST"])
@inject_user()
@protected_sec(redirect_on_fail=True)
async def make_transaction(request, user):
    """Make a transaction endpoint."""

    date = datetime.strptime(
        f'{request.json.get("tx_date")}'
        f' {request.json.get("tx_time")}',
        "%d/%m/%Y %H:%M",
    )

    storage = request.ctx.storage

    result = await storage.make_transaction(
        user_id=user["id"],
        kind=request.json.get("action"),
        amount=request.json.get("amount"),
        coin=request.json.get("currency"),
        price=request.json.get("price"),
        date=date,
    )

    if isinstance(result, Error):
        return json("Can't create transaction", status=400)

    return json({}, status=201)
