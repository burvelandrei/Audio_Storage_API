import factory
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, AudioFile

fake = Faker()


class AsyncSQLAlchemyModelFactory(factory.Factory):
    """Асинхронная фабрика для моделей"""

    class Meta:
        abstract = True

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        obj = cls.build(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj


class UserFactory(AsyncSQLAlchemyModelFactory):
    """Фабрика для пользователей"""

    class Meta:
        model = User

    yandex_id = factory.Faker("uuid4")
    username = factory.Faker('user_name')
    is_admin = False


class AudioFileFactory(AsyncSQLAlchemyModelFactory):
    """Фабрика для аудиофайлов"""

    class Meta:
        model = AudioFile

    filename = factory.Faker("file_name")
    filepath = factory.Faker("file_path")
    owner_id = None
