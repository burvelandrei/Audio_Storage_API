import httpx
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db.operations import UserDO
from db.connect import get_session
from schemas.user import RefreshTokenRequest
from services.auth import create_access_token, create_refresh_token
from config import settings


router = APIRouter(prefix="/auth")


# Перенаправление на авторизацию Яндекса
@router.get("/yandex/")
async def auth_yandex():
    auth_url = (
        f"https://oauth.yandex.ru/authorize?"
        f"response_type=code&client_id={settings.YANDEX_CLIENT_ID}&"
        f"redirect_uri={settings.REDIRECT_URI}"
    )
    return RedirectResponse(auth_url)


# Приём ответа после авторизации
@router.get("/yandex/callback/")
async def auth_yandex_callback(
    code: str,
    session: AsyncSession = Depends(get_session),
):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
                "redirect_uri": settings.REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if token_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error getting token",
        )

    token_data = token_response.json()
    yandex_access_token = token_data["access_token"]

    async with httpx.AsyncClient() as client:
        user_info_response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {yandex_access_token}"},
        )

    if user_info_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error getting user data",
        )

    user_data = user_info_response.json()
    yandex_id = user_data["id"]
    username = user_data.get("login", "unknown")

    user = await UserDO.get_by_yandex_id(yandex_id=yandex_id, session=session)

    if not user:
        user = await UserDO.add(
            session=session,
            **{
                "yandex_id": yandex_id,
                "username": username,
            },
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )


# Обновление access токена
@router.post("/token/refresh/")
async def refresh_access_token(
    token_data: RefreshTokenRequest,
):
    invalid_refresh_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
    )
    try:
        payload = jwt.decode(
            token_data.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise invalid_refresh_token_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )
    except jwt.PyJWTError:
        raise invalid_refresh_token_exception
    new_access_token = create_access_token(data={"sub": str(user_id)})
    return JSONResponse(
        content={
            "access_token": new_access_token,
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )
