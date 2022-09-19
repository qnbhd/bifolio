from bifolio.main import app as application
import pytest


@pytest.fixture
def app():
    yield application
