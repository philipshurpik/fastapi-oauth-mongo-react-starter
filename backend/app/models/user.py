from datetime import datetime
from typing import List

from beanie import Indexed, Link
from fastapi_users.db import BaseOAuthAccount
from fastapi_users_db_beanie import BeanieBaseUserDocument
from pydantic import EmailStr, Field

from .item import Item


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUserDocument):
    email: Indexed(EmailStr, unique=True)  # type: ignore
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    hashed_password: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    items: List[Link[Item]] = []

    def __repr__(self):
        return f"User(id={self.id!r}, email={self.email!r})"
