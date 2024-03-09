from datetime import datetime
from typing import Any, List

from beanie import SortDirection
from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from ..deps.request_params import ItemRequestParams
from ..deps.users import CurrentUser
from ..models.item import Item
from ..schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items")


@router.get("", response_model=List[ItemResponse])
async def get_items(
    response: Response,
    request_params: ItemRequestParams,
    user: CurrentUser,
) -> Any:
    # Fetch items with pagination and sorting
    items_query = Item.find(Item.user_id == user.id)
    if request_params.sort:
        field, direction = request_params.sort
        sort_direction = SortDirection.ASCENDING if direction == 1 else SortDirection.DESCENDING
        items_query = items_query.sort((field, sort_direction))
    items = await items_query.skip(request_params.skip).limit(request_params.limit).to_list()

    # Get the total count of items for pagination headers
    total = await Item.find(Item.user_id == user.id).count()
    response.headers["Content-Range"] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return [x.dict() for x in items]


@router.post("", response_model=ItemResponse, status_code=201)
async def create_item(
    item_in: ItemCreate,
    user: CurrentUser,
) -> Any:
    item_dict = item_in.dict()
    item_dict["user_id"] = user.id
    item = Item(**item_dict)
    await item.create()
    return item.dict()


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,  # Beanie uses string representations for MongoDB's ObjectId
    item_in: ItemUpdate,
    user: CurrentUser,
) -> Any:
    item = await Item.get(item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item_in.dict(exclude_unset=True)
    update_data["updated"] = datetime.utcnow()
    await item.set(update_data)
    return item.dict()


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,  # Beanie uses string representations for MongoDB's ObjectId
    user: CurrentUser,
) -> Any:
    item = await Item.get(item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.dict()


@router.delete("/{item_id}")
async def delete_item(
    item_id: str,  # Beanie uses string representations for MongoDB's ObjectId
    user: CurrentUser,
) -> Any:
    item = await Item.get(item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    await item.delete()  # type: ignore
    return {"success": True}
