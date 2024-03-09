import json
from typing import Annotated, Callable, Optional

from fastapi import Depends, HTTPException, Query

from ..schemas.request_params import RequestParams


def parse_react_admin_params() -> Callable:
    """Parses sort and range parameters coming from a react-admin request"""

    async def inner(
        sort_: Optional[str] = Query(
            None,
            alias="sort",
            description='Format: `["field_name", "ASC|DESC"]`',
            example='["id", "ASC"]',
        ),
        range_: Optional[str] = Query(
            None,
            alias="range",
            description="Format: `[start, end]`",
            example="[0, 10]",
        ),
    ) -> RequestParams:
        skip, limit = 0, 10
        if range_:
            start, end = json.loads(range_)
            skip, limit = start, end - start + 1

        sort_params = None
        if sort_:
            sort_field, sort_order = json.loads(sort_)
            if sort_order.upper() not in ["ASC", "DESC"]:
                raise HTTPException(400, f"Invalid sort direction {sort_order}")
            sort_params = (sort_field, 1 if sort_order.upper() == "ASC" else -1)

        return RequestParams(skip=skip, limit=limit, sort=sort_params)

    return inner


ItemRequestParams = Annotated[RequestParams, Depends(parse_react_admin_params())]
