"""Module contains the main web-application for bifolio."""
from importlib import import_module
import logging
from pathlib import Path
import sys
import warnings

from rich.traceback import install
from sanic import Sanic
from sanic.response import redirect


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from sanic_openapi import openapi2_blueprint

from sqlalchemy.ext.asyncio import create_async_engine


log = logging.getLogger("bifolio")


modules = ()


def create_app(module_names=None):
    """
    Create the bifolio application.

    Args:
        module_names: List of modules to import.

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

    bind = create_async_engine(
        "sqlite+aiosqlite:///test.db", echo=True
    )

    app.static(
        "/static",
        Path(__file__).parent / "static" / "tailwindcss" / "src",
    )

    @app.route("/", methods=["GET", "POST"])
    async def root(request):
        if request.ctx.session.get("loggedin"):
            return redirect("/home")
        return redirect("/account/login")

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
    sanic_app.run(auto_reload=True, workers=4)
