from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession


from src.core.schemas import APIErrorMessage
from src.lessons.repository import LessonsRepository
from src.lessons.schemas import LessonSchema
import src.core.dependencies as core_deps

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
)


@router.get(
    "/",
    response_model=List[LessonSchema],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_lessons_list(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
) -> JSONResponse:
    """Получение списка уроков"""
    repository = LessonsRepository(session=session)
    lesson_list = await repository.get_all()
    response_data = [LessonSchema.model_validate(l).model_dump() for l in lesson_list]

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.get(
    "/{id}",
    response_model=LessonSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_lesson_by_id(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    id: int,
) -> JSONResponse:
    """Получение урока по id"""

    repository = LessonsRepository(session=session)
    lesson = await repository.get_one(id=id)
    response_data = LessonSchema.model_validate(lesson).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.delete(
    "/{id}",
    response_model=str,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def delete_lesson_by_id(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    id: int,
) -> JSONResponse:
    """Удаление урока по id"""

    repository = LessonsRepository(session=session)
    deleted_lesson_id = await repository.delete_one(id=id)
    response_data = {"deleted": deleted_lesson_id}

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
