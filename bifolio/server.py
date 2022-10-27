"""Module contains the main web-application for bifolio."""
from importlib import import_module
import logging
import os
from pathlib import Path
import sys
import warnings

from rich.traceback import install
from sanic import Sanic


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from sanic_openapi import openapi2_blueprint

from sqlalchemy.ext.asyncio import create_async_engine


log = logging.getLogger("bifolio")


modules = (
    "bifolio.blueprints.account",
    "bifolio.blueprints.home",
    "bifolio.blueprints.api",
    "bifolio.blueprints.profile",
    "bifolio.blueprints.transactions",
)


def create_app(
    module_names=None, db_url=None, workers=1, redis_url=None
):
    """
    Create the bifolio application.

    Args:
        module_names: List of modules to import.
        db_url: Database URL.
        redis_url: Redis URL.

    Returns:
        Sanic application.

    """

    from sanic_cors import CORS

    from bifolio.auth import setup_auth
    from bifolio.config import update_config
    from bifolio.middlewares.session import setup_session_middlewares
    from bifolio.tools.j2 import setup_jinja

    install()

    app = Sanic("bifolio")

    db_url = db_url or "sqlite+aiosqlite:///test.db"

    bind = create_async_engine(db_url, echo=True)

    app.static(
        "/static",
        Path(__file__).parent / "static" / "tailwindcss" / "src",
    )

    @app.route("/", methods=["GET", "POST"])
    async def root(request):
        return request.app.ctx.j2.render("index.html", request)

    module_names = module_names or modules

    for module_name in module_names:
        module = import_module(module_name)
        sys.modules[module.__name__] = module

        bp = getattr(module, "bp", None)

        if bp:
            print(f"Registering blueprint `{bp.name}`")
            app.blueprint(bp)

    update_config(app)
    setup_session_middlewares(app, bind)
    app.blueprint(openapi2_blueprint)
    setup_jinja(app)
    setup_auth(app)

    CORS(app)

    return app


if __name__ == "__main__":
    sanic_app = create_app()
    sanic_app.run(
        host=os.getenv("BIFOLIO_HOST", "localhost"),
        port=int(os.getenv("BIFOLIO_PORT", 8000)),
        auto_reload=True,
        workers=4,
    )
