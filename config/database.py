from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from .settings import settings


class DataBaseHelper:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )

        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def session(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            yield session

db_helper = DataBaseHelper(
    url=settings.db_settings.URL,
    echo=settings.db_settings.ECHO,
)