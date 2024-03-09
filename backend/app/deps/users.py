from typing import Annotated

from beanie.odm.fields import PydanticObjectId
from fastapi import Depends
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.manager import BaseUserManager
from fastapi_users_db_beanie import BeanieUserDatabase, ObjectIDIDMixin
from starlette.requests import Request
from starlette.responses import Response

from ..core.config import settings
from ..models.user import OAuthAccount
from ..models.user import User as UserModel

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


jwt_authentication = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(ObjectIDIDMixin, BaseUserManager[UserModel, PydanticObjectId]):
    user_db_model = UserModel
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY


async def get_user_db():
    yield BeanieUserDatabase(UserModel, OAuthAccount)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(get_user_manager, [jwt_authentication])

CurrentUser = Annotated[UserModel, Depends(fastapi_users.current_user(active=True))]
CurrentSuperuser = Annotated[UserModel, Depends(fastapi_users.current_user(active=True, superuser=True))]
