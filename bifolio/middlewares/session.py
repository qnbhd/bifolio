from contextvars import ContextVar
import logging

import aioredis
import secure
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bifolio.storage.rdb import SQLAlchemyStorage
from bifolio.tools.returns import Error


_base_model_session_ctx: ContextVar[str] = ContextVar("_db_session")

log = logging.getLogger(__name__)


def setup_session_middlewares(app, bind):
    """Setup session middlewares."""

    secure_headers = secure.Secure()

    # noinspection PyProtectedMember
    @app.middleware("request")
    async def inject_session(request):
        """Inject session."""

        request.ctx._db_session = sessionmaker(
            bind, AsyncSession, expire_on_commit=False
        )()
        request.ctx._db_session_ctx_token = (
            _base_model_session_ctx.set(request.ctx._db_session)
        )
        result = await SQLAlchemyStorage.create(
            bind, request.ctx._db_session
        )

        if isinstance(result, Error):
            log.error(result.message)
            exit(0)

        request.ctx.storage = result.result

    # noinspection PyProtectedMember
    @app.middleware("response")
    async def close_session(request, response):
        """Close session."""

        secure_headers.framework.sanic(response)

        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(
                request.ctx._db_session_ctx_token
            )
            await request.ctx._db_session.close()

    @app.listener("before_server_start")
    async def server_init(app_, loop):
        """Server init."""

        app_.ctx.redis = await aioredis.from_url(
            app_.config["redis"], decode_responses=True
        )
