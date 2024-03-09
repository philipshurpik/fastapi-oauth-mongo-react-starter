from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[PydanticObjectId]):
    items_count: Optional[int] = Field(None, description="The number of items associated with the user")


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
