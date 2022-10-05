import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import constr


class UserModel(BaseModel):

    id: Optional[int]
    username: constr(min_length=4, max_length=20)  # type: ignore
    password: constr(min_length=8, max_length=100)  # type: ignore

    class Config:
        orm_mode = True


class TransactionModel(BaseModel):

    user_id: int
    kind: str
    coin: str
    amount: float
    price: float
    date: datetime.datetime

    class Config:
        orm_mode = True
