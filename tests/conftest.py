import logging

import pytest
from sanic_testing import TestManager

from bifolio.server import create_app


@pytest.fixture
def app():
    sanic_app = create_app()
    TestManager(sanic_app)
    return sanic_app


@pytest.fixture
def logger():
    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, "DEBUG", None)
    logger.setLevel(numeric_level)
    return logger
