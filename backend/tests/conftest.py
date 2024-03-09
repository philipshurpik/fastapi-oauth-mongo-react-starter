import pytest
from beanie import init_beanie as init_beanie_default
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.factory import create_app
from app.models.item import Item
from app.models.user import User

from .utils import create_test_item, create_test_user, generate_random_string


@pytest.fixture(scope="function")
async def mongo_client():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    yield client
    client.close()


@pytest.fixture(scope="function")
async def init_beanie(mongo_client):
    db = mongo_client[settings.MONGODB_DB_NAME]
    await init_beanie_default(database=db, document_models=[User, Item])


@pytest.fixture(scope="function")
async def app(init_beanie):
    application = create_app()
    yield application


@pytest.fixture(scope="function")
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def test_user():
    user = await create_test_user()
    yield user
    await user.delete()  # type: ignore


@pytest.fixture(scope="function")
async def test_item(test_user):
    item = await create_test_item(user=test_user)
    yield item
    await item.delete()  # type: ignore


@pytest.fixture(scope="function")
def default_password():
    return generate_random_string(32)
