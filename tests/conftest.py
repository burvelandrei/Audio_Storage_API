import pytest
import pytest_asyncio
import asyncio
import respx
from httpx import AsyncClient, ASGITransport, Response
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from main import app
from db.models import Base
from db.connect import get_session
from services.auth import create_access_token
from tests.factories import UserFactory, AudioFileFactory
from config import settings


# Настройки PostgreSQL
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    """
    Используем общий event loop
    """
    loop = asyncio.get_event_loop()
    yield loop


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Фикстура для БД, создаёт и удаляет таблицы"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session():
    """Фикстура для сессии"""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(test_session):
    """Подмена зависимостей и тестовый клиент"""
    app.dependency_overrides[get_session] = lambda: test_session
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
def mock_yandex():
    """Мокирование запросов к yandex"""
    with respx.mock:
        respx.post("https://oauth.yandex.ru/token").mock(
            return_value=Response(
                200,
                json={"access_token": "mock_access_token"},
            )
        )
        respx.get("https://login.yandex.ru/info").mock(
            return_value=Response(
                200,
                json={"id": "123456", "login": "testuser"},
            )
        )
        yield


@pytest_asyncio.fixture
async def user(test_session: AsyncSession):
    """Фикстура для создания пользователя"""
    user = await UserFactory.create_async(session=test_session)
    yield user
    await test_session.rollback()


@pytest_asyncio.fixture
async def user_headers(user):
    """Заголовки для пользователя"""
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    return user, headers


@pytest_asyncio.fixture
async def admin(test_session: AsyncSession):
    """Фикстура для создания администратора"""
    admin = await UserFactory.create_async(
        session=test_session,
        is_admin=True,
    )
    yield admin
    await test_session.rollback()


@pytest_asyncio.fixture
async def admin_headers(admin):
    """Заголовки для администратора"""
    token = create_access_token({"sub": str(admin.id)})
    headers = {"Authorization": f"Bearer {token}"}
    return admin, headers


@pytest_asyncio.fixture
async def audio_file(test_session: AsyncSession, user_headers):
    """Фикстура для создания аудиофайлов"""
    user, _ = user_headers
    files = []
    for _ in range(3):
        await AudioFileFactory.create_async(
            session=test_session,
            owner_id=user.id,
        )
    yield files
    await test_session.rollback()
