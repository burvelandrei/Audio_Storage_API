import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, user, admin_headers):
    _, headers = admin_headers
    response = await client.get(f"/users/{user.id}/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["username"] == user.username


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, user, admin_headers):
    _, headers = admin_headers
    new_username = "updated_username"
    response = await client.patch(
        f"/users/{user.id}/", json={"username": new_username}, headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == new_username


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, user, admin_headers):
    _, headers = admin_headers
    response = await client.delete(f"/users/{user.id}/", headers=headers)

    assert response.status_code == 204
