from typing import Annotated, List

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.schemas import APIErrorMessage
from src.core.logger import logger
from src.lessons.repository import LessonsRepository
from src.lessons.shemas import LessonSchema
import src.core.dependencies as core_deps

router = APIRouter()


# Read


@router.get(
    "/lessons",
    response_model=List[LessonSchema],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    tags=["search"],
)
@cache(expire=5)
async def lessons_list(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    query: str = Query(
        None,
        examples=[
            "",
        ],
        description="Список уроков",
    ),
) -> JSONResponse:
    """Получение списка уроков"""

    logger.debug(f"lessons_list query:{query}")
    repository = LessonsRepository(session=session)
    lesson_list = await repository.get_all()
    response_data = [LessonSchema.model_validate(l).model_dump() for l in lesson_list]

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
