from beanie import init_beanie
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from httpx_oauth.clients.google import GoogleOAuth2
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse

from .api import api_router
from .core.config import settings
from .deps.users import fastapi_users, jwt_authentication
from .models import Item, User
from .schemas.user import UserCreate, UserRead, UserUpdate


def create_app():
    description = f"{settings.PROJECT_NAME} API"
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PATH}/openapi.json",
        docs_url="/docs/",
        description=description,
        redoc_url=None,
    )
    setup_routers(app, fastapi_users)
    setup_cors_middleware(app)
    serve_static_app(app)
    return app


async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL, uuidRepresentation="standard")
    db = client[settings.MONGODB_DB_NAME]
    return await init_beanie(
        database=db,
        document_models=[User, Item],
    )


def setup_routers(app: FastAPI, fastapi_users: FastAPIUsers) -> None:
    app.include_router(api_router, prefix=settings.API_PATH)
    google_oauth_client = GoogleOAuth2(settings.GOOGLE_OAUTH_CLIENT_ID, settings.GOOGLE_OAUTH_CLIENT_SECRET)
    redirect_url = f"{settings.FRONTEND_URL}/oauth-callback"
    app.include_router(
        fastapi_users.get_oauth_router(
            google_oauth_client,
            jwt_authentication,
            state_secret=settings.SECRET_KEY,
            associate_by_email=True,
            redirect_url=redirect_url,
        ),
        prefix=f"{settings.API_PATH}/auth/google",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_auth_router(
            jwt_authentication,
            requires_verification=False,
        ),
        prefix=f"{settings.API_PATH}/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix=f"{settings.API_PATH}/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=False),
        prefix=f"{settings.API_PATH}/users",
        tags=["users"],
    )
    # The following operation needs to be at the end of this function
    use_route_names_as_operation_ids(app)


def serve_static_app(app):
    app.mount("/", StaticFiles(directory="static"), name="static")

    @app.middleware("http")
    async def _add_404_middleware(request: Request, call_next):
        """Serves static assets on 404"""
        response = await call_next(request)
        path = request["path"]
        if path.startswith(settings.API_PATH) or path.startswith("/docs"):
            return response
        if response.status_code == 404:
            return FileResponse("static/index.html")
        return response


def setup_cors_middleware(app):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    route_names = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in route_names:
                raise Exception("Route function names should be unique")
            route.operation_id = route.name
            route_names.add(route.name)
