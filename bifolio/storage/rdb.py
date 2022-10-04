from typing import List

from sqlalchemy import select
import sqlalchemy.exc

from bifolio import models
from bifolio.database.models import Base
from bifolio.database.models import Transaction
from bifolio.database.models import User
from bifolio.storage.storage import Storage
from bifolio.tools.returns import Error
from bifolio.tools.returns import Ok
from bifolio.tools.returns import Result


class SQLAlchemyStorage(Storage):
    def __init__(self, session):
        self.session = session

    @classmethod
    async def create(
        cls, bind, session
    ) -> Result["SQLAlchemyStorage"]:
        try:
            async with bind.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except (Exception, sqlalchemy.exc.SQLAlchemyError) as e:
            return Error(message=str(e))

        return Ok(cls(session))

    async def get_user(
        self, login, method="id"
    ) -> Result[models.UserModel]:
        async with self.session.begin():

            if method == "id":
                stmt = select(User).where(User.id == login)
            elif method == "login":
                stmt = select(User).where(User.login == login)
            else:
                return Error(message="Unknown method")

            try:
                result = await self.session.execute(stmt)
            except Exception as e:
                return Error(message=str(e))

        row = result.one_or_none()

        if not row:
            return Error(message="User not found")

        user = row[0]

        return Ok(
            models.UserModel(
                id=user.id,
                username=user.login,
                password=user.password,
            )
        )

    async def get_users(self) -> Result[List[models.UserModel]]:

        async with self.session.begin():
            stmt = select(User)
            result = await self.session.execute(stmt)

        rows = result.all()

        return Ok([models.UserModel.from_orm(row[0]) for row in rows])

    async def create_user(
        self, username, password
    ) -> Result[models.UserModel]:
        try:
            async with self.session.begin():
                user = User(login=username, password=password)
                self.session.add(user)

            await self.session.commit()
        except Exception as e:
            return Error(message=str(e))

        return Ok(
            models.UserModel(
                id=user.id,
                username=user.login,
                password=user.password,
            )
        )

    async def get_user_transactions(
        self, user_id
    ) -> Result[List[models.TransactionModel]]:
        async with self.session.begin():
            stmt = select(Transaction).where(
                Transaction.user_id == user_id
            )
            result = await self.session.execute(stmt)

        rows = result.all()

        return Ok(
            [models.TransactionModel.from_orm(row[0]) for row in rows]
        )

    async def make_transaction(
        self, user_id, kind, amount, coin, price, date
    ) -> Result[models.TransactionModel]:
        try:
            async with self.session.begin():
                tx = Transaction(
                    user_id=user_id,
                    kind=kind,
                    amount=amount,
                    coin=coin,
                    price=price,
                    date=date,
                )

                self.session.add(tx)
        except Exception as e:
            return Error(message=str(e))

        return Ok(models.TransactionModel.from_orm(tx))
