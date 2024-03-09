from typing import Any, List

from fastapi.routing import APIRouter
from starlette.responses import Response

from ..deps.users import CurrentSuperuser
from ..models.user import User
from ..schemas.user import UserRead

router = APIRouter()


@router.get("/users", response_model=List[UserRead])
async def get_users(
    response: Response,
    user: CurrentSuperuser,  # Ensure this dependency aligns with your auth setup
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = await User.find().skip(skip).limit(limit).to_list()
    total = await User.find().count()
    response.headers["Content-Range"] = f"{skip}-{skip + len(users)}/{total}"
    return users
