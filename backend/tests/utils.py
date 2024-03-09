import secrets
import string
import uuid
from typing import Any

from fastapi_users.jwt import generate_jwt

from app.deps.users import get_jwt_strategy
from app.models import Item, User


def generate_random_string(length: int) -> str:
    return "".join(secrets.choice(string.ascii_lowercase) for i in range(length))


def get_jwt_header(user: User) -> Any:
    jwt_strategy = get_jwt_strategy()
    data = {"sub": str(user.id), "aud": jwt_strategy.token_audience}
    token = generate_jwt(data, jwt_strategy.secret, jwt_strategy.lifetime_seconds)
    return {"Authorization": f"Bearer {token}"}


async def create_test_user(email: str = "test@example.com", password: str = "testpassword") -> User:
    # Assuming your User model has a hashed_password field and possibly other required fields
    user = User(
        email=email.replace("@", f"_{str(uuid.uuid4()).split('-')[-1]}@"),
        hashed_password=password,
    )
    await user.create()
    return user


async def create_test_item(user: User, value: str = "Test Item") -> Item:
    item = Item(
        user_id=user.id,
        value=value,
    )
    await item.create()
    return item
