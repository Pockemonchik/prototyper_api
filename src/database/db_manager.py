from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.logger import logger


class AsyncPostgresDatabaseManager:
    """Менеджер по работе с бд"""

    def __init__(self, url: str, echo: bool = False):
        try:
            self.engine = create_async_engine(
                url=url,
                echo=echo,
            )
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )
            logger.info("PG DB conn success")
        except Exception as e:
            logger.info(f"Err when con {e}")

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session
            logger.debug("session close")
            await session.close()
