from datetime import datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Item(Document):
    user_id: Indexed(PydanticObjectId)  # type: ignore
    value: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "items"
