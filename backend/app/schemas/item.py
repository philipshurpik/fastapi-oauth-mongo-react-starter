from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    value: str


class ItemUpdate(ItemCreate):
    pass


class Item(ItemCreate):
    user_id: PydanticObjectId
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class ItemResponse(Item):
    id: PydanticObjectId
