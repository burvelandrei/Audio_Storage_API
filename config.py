from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    REDIRECT_URI: str = ""

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

    def __init__(self, **data):
        super().__init__(**data)
        if self.REDIRECT_URI is None:
            self.REDIRECT_URI = (
                f"http://{self.SERVER_HOST}:{self.SERVER_PORT}"
                "/auth/yandex/callback/"
            )


settings = Settings()
