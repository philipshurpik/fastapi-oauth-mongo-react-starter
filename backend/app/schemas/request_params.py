from typing import Optional, Tuple

from pydantic import BaseModel


class RequestParams(BaseModel):
    skip: int = 0
    limit: int = 10
    sort: Optional[Tuple[str, int]] = None
