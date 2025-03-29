from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    REDIRECT_URI: str = (
        f"http://{SERVER_HOST}:{SERVER_PORT}/auth/yandex/callback/"
    )

    UPLOAD_DIR: str = "uploads"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
