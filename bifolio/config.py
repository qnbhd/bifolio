import os
from pathlib import Path


def update_config(app):
    """Update config.

    Args:
        app: Sanic application.

    """

    app.config["API_VERSION"] = "0.0.1"
    app.config["API_TITLE"] = "BiFolio"
    app.config["API_LICENSE_NAME"] = "MIT"
    app.config["API_CONTACT_EMAIL"] = "1qnbhd@gmail.com"
    app.config["API_DESCRIPTION"] = (
        "BiFolio is a web-application"
        " for tracking your crypto-portfolio."
    )
    app.config["TEMPLATING_PATH_TO_TEMPLATES"] = (
        Path(__file__).parent / "static" / "tailwindcss" / "src"
    )
    app.config["redis"] = "redis://localhost"
    app.config["SANIC_JWT_SECRET"] = os.getenv(
        "SANIC_JWT_SECRET", "secret"
    )
