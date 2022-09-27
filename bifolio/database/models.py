"""Module that contains the database models for the Bifolio application."""

import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import INTEGER
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


class TransactKind(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


Base = declarative_base()


class BaseModel(Base):  # type: ignore
    """Base model for all models."""

    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)


class User(BaseModel):
    """User model."""

    __tablename__ = "user"

    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Transaction(BaseModel):
    """Transaction model."""

    __tablename__ = "transaction"

    user_id = Column(
        ForeignKey(User.id), doc="User identifier."
    )  # type: ignore
    user = relationship(User, backref="transactions")  # type: ignore

    kind = Column(
        Enum(TransactKind),
        doc="Transaction kind. Can be `BUY`, `SELL`.",
    )  # type: ignore
    coin = Column(String, nullable=False, doc="Coin name.")
    amount = Column(
        Float, nullable=False, doc="Amount of coin transaction."
    )
    price = Column(
        Float, nullable=False, doc="Transaction price at `date`."
    )  # in usd
    date = Column(DateTime, nullable=False, doc="Transaction date.")
