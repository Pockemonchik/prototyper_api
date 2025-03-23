from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

import src.core.dependencies as core_deps
import src.users.dependencies as users_deps
from src.core.logger import logger
from src.core.schemas import APIErrorMessage
from src.lessons.repository import LessonsRepository, LessonsStepRepository
from src.lessons.schemas import LessonSchema, LessonStepSchema

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
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
) -> JSONResponse:
    """Получение списка уроков"""
    logger.debug("get_lessons_list user_id={user_id}")
    repository = LessonsRepository(session=session)
    lesson_list = await repository.get_all_lessons_with_user_results(user_id=user_id)
    response_data = [lesson.model_dump() for lesson in lesson_list]

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
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
    id: int,
) -> JSONResponse:
    """Получение урока по id"""
    logger.debug("get_lesson_by_id user_id={user_id}")
    repository = LessonsRepository(session=session)
    lesson = await repository.get_one_lesson_with_steps(
        user_id=user_id,
        lesson_id=id,
    )
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
    logger.debug("delete_lesson_by_id")
    repository = LessonsRepository(session=session)
    deleted_lesson_id = await repository.delete_one(id=id)
    response_data = {"deleted": deleted_lesson_id}

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.get(
    "/{id}/steps/{step_id}",
    response_model=LessonSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_lesson_step_by_id(
    session: Annotated[
        AsyncSession,
        Depends(core_deps.get_session),
    ],
    id: int,
    step_id: int,
) -> JSONResponse:
    """Получение урока по id"""
    logger.debug("get_lesson_step_by_id  user_id={user_id} step_id={step_id} ")
    repository = LessonsStepRepository(session=session)
    step = await repository.get_lesson_step_with_texts(
        step_id=step_id,
    )
    response_data = LessonStepSchema.model_validate(step).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
