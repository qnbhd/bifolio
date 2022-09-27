from contextvars import ContextVar

import aioredis
from sanic_session import AIORedisSessionInterface
from sanic_session import Session
import secure
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


_base_model_session_ctx: ContextVar[str] = ContextVar("db_session")


def setup_session_middlewares(app, bind):
    """Setup session middlewares."""

    from bifolio.database.models import Base

    secure_headers = secure.Secure()

    session = Session()

    @app.middleware("request")
    async def inject_session(request):
        """Inject session."""

        request.ctx.db_session = sessionmaker(
            bind, AsyncSession, expire_on_commit=False
        )()
        request.ctx.db_session_ctx_token = (
            _base_model_session_ctx.set(request.ctx.db_session)
        )

        async with bind.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.middleware("response")
    async def close_session(request, response):
        """Close session."""

        secure_headers.framework.sanic(response)

        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(
                request.ctx.db_session_ctx_token
            )
            await request.ctx.db_session.close()

    @app.listener("before_server_start")
    async def server_init(app_, loop):
        """Server init."""

        app_.ctx.redis = await aioredis.from_url(
            app_.config["redis"], decode_responses=True
        )

        session.init_app(
            app, interface=AIORedisSessionInterface(app_.ctx.redis)
        )
