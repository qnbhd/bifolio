import abc
from typing import List

from bifolio import models
from bifolio.tools.returns import Result


class Storage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_user(
        self, login, method="id"
    ) -> Result[models.UserModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_users(self) -> Result[List[models.UserModel]]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_user(
        self, username, password
    ) -> Result[models.UserModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_user_transactions(
        self, login
    ) -> Result[List[models.TransactionModel]]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def make_transaction(
        self, user_id, kind, amount, coin, price, date
    ) -> Result[models.TransactionModel]:
        raise NotImplementedError()
