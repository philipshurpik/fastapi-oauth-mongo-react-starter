from uuid import uuid4

import pytest
from pydantic import EmailStr

from app.models.user import User


@pytest.mark.asyncio
async def test_user_model(init_beanie):
    user_mail = f"test_{str(uuid4()).split('-')[-1]}@example.com"
    user = User(email=EmailStr(user_mail), hashed_password="1234")
    try:
        await user.create()  # Use Beanie's create method to insert the document
        fetched_user = await User.get(user.id)  # Retrieve the user document by ID

        assert fetched_user is not None
        assert fetched_user.id == user.id
        assert fetched_user.email == user_mail
        assert fetched_user.hashed_password == "1234"
    finally:
        if user.id:
            await user.delete()  # type: ignore
