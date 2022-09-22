import pytest

from bifolio.main import app as application


@pytest.fixture
def app():
    yield application
