import logging
import unittest.mock

import pytest
from sanic_testing import TestManager

from bifolio.server import create_app


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]

    def pop(cls, *args, **kwargs):
        if cls in cls._instances:
            return cls._instances.pop(cls)
        return None


class RedisMock(metaclass=Singleton):
    def __init__(self):
        self.key_value = dict()

    @classmethod
    async def from_url(cls, url, **kwargs):
        return cls()

    async def get(self, key, *args, default=None, **kwargs):
        return self.key_value.get(key)

    async def set(self, key, value, *args, **kwargs):
        self.key_value[key] = value

    async def delete(self, key, *args, **kwargs):
        self.key_value.pop(key, None)

    async def exists(self, key, *args, **kwargs):
        return key in self.key_value


@pytest.fixture
def app():
    Singleton.pop(RedisMock)
    with unittest.mock.patch(
        "aioredis.from_url", new=RedisMock.from_url
    ):
        sanic_app = create_app(db_url="sqlite+aiosqlite:///:memory:")
        TestManager(sanic_app)
        yield sanic_app


@pytest.fixture
def logger():
    logger = logging.getLogger(__name__)
    numeric_level = getattr(logging, "DEBUG", None)
    logger.setLevel(numeric_level)
    return logger
