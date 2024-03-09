import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.schemas.item import ItemResponse

from ..utils import create_test_item, create_test_user, get_jwt_header


@pytest.fixture
async def test_user():
    user = await create_test_user()
    yield user
    await user.delete()  # type: ignore


@pytest.fixture
async def test_item(test_user):
    item = await create_test_item(user=test_user)
    yield item
    await item.delete()  # type: ignore


class TestGetItems:
    @pytest.mark.asyncio
    async def test_get_items_not_logged_in(self, client: AsyncClient):
        resp = await client.get(f"{settings.API_PATH}/items")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_get_items(self, client: AsyncClient, test_user, test_item):
        jwt_header = get_jwt_header(test_user)
        resp = await client.get(f"{settings.API_PATH}/items", headers=jwt_header)
        assert resp.status_code == 200
        assert "Content-Range" in resp.headers
        items = resp.json()
        assert len(items) >= 1  # Assuming there could be other items in the test DB
        assert any(item["id"] == str(test_item.id) for item in items)


class TestGetSingleItem:
    @pytest.mark.asyncio
    async def test_get_single_item(self, client: AsyncClient, test_user, test_item):
        jwt_header = get_jwt_header(test_user)
        resp = await client.get(f"{settings.API_PATH}/items/{str(test_item.id)}", headers=jwt_header)
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == str(test_item.id)
        assert data["value"] == test_item.value


class TestCreateItem:
    @pytest.mark.asyncio
    async def test_create_item(self, client: AsyncClient, test_user):
        jwt_header = get_jwt_header(test_user)
        resp = await client.post(f"{settings.API_PATH}/items", headers=jwt_header, json={"value": "value"})
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data


class TestDeleteItem:
    @pytest.mark.asyncio
    async def test_delete_item(self, client: AsyncClient, test_user, test_item):
        jwt_header = get_jwt_header(test_user)
        resp = await client.delete(f"{settings.API_PATH}/items/{str(test_item.id)}", headers=jwt_header)
        assert resp.status_code == 200

    @pytest.mark.asyncio
    async def test_delete_item_does_not_exist(self, client: AsyncClient, test_user):
        jwt_header = get_jwt_header(test_user)
        resp = await client.delete(f"{settings.API_PATH}/items/5f9b3b3b9d9f3d0001a3b3b3", headers=jwt_header)
        assert resp.status_code == 404


class TestUpdateItem:
    @pytest.mark.asyncio
    async def test_update_item(self, client: AsyncClient, test_user, test_item):
        jwt_header = get_jwt_header(test_user)
        resp = await client.put(
            f"{settings.API_PATH}/items/{str(test_item.id)}", headers=jwt_header, json={"value": "new value"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["value"] == "new value"
