import pytest
import jwt
from httpx import AsyncClient
from config import settings


@pytest.mark.asyncio
async def test_auth_yandex_callback(client: AsyncClient, mock_yandex):
    response = await client.get(
        "/auth/yandex/callback/",
        params={"code": "mock_code"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_access_token(
    client: AsyncClient,
    user,
):

    refresh_token = jwt.encode(
        {"sub": str(user.id)},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    response = await client.post(
        "/auth/token/refresh/",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_access_token_invalid(client: AsyncClient):
    response = await client.post(
        "/auth/token/refresh/", json={"refresh_token": "invalidtoken"}
    )

    assert response.status_code == 401
