from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.logger import logger


class AsyncPostgresDatabaseManager:
    def __init__(self, url: str, echo: bool = False):
        try:
            self.engine = create_async_engine(
                url=url,
                echo=echo,
            )
            logger.info("PG DB conn success")
        except Exception as e:
            logger.info(f"Err when con {e}")

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def get_async_session(self) -> AsyncGenerator[async_sessionmaker, None]:
        async with self.session_factory as session:  # type: ignore
            yield session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(
        self,
    ) -> AsyncGenerator[async_scoped_session, None]:
        session = self.get_scoped_session()
        yield session
        await session.close()
