from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    yandex_id: str
    username: str
    is_admin: bool


class UserModify(BaseModel):
    username: str | None = None
    is_admin: bool | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
