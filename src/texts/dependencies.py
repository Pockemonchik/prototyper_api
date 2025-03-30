from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.texts.repository import TextRepository

from src.texts.service import TextService


async def get_text_service_dep(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TextService:
    """Получение сервиса lessons"""
    text_repo = TextRepository(session=session)
    service = TextService(
        text_repo=text_repo,
    )
    return service
