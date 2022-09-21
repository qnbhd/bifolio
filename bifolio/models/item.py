"""Module contains the item model."""

from pydantic import BaseModel


__all__ = ["Item"]


class Item(BaseModel):
    """This is a simple model for testing."""

    value: int
