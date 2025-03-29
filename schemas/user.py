from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    yandex_id: str
    username: str
    is_admin: bool


class UserModify(BaseModel):
    username: str
    is_admin: bool


class RefreshTokenRequest(BaseModel):
    refresh_token: str
