from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

import src.lessons.dependencies as lessons_deps
import src.users.dependencies as users_deps
from src.core.logger import logger
from src.core.schemas import APIErrorMessage
from src.database.base_schemas import DbEntityBaseSchema
from src.lessons.schemas import (
    CreateLessonSchema,
    CreateLessonStepForm,
    LessonSchema,
    LessonStepSchema,
    SetLessonStepResultForm,
)
from src.lessons.service import LessonsService

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
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
) -> JSONResponse:
    """Получение списка уроков"""
    logger.debug("get_lessons_list user_id={user_id}")
    lesson_list = await lesson_service.get_all_lessons_with_user_results(
        user_id=user_id
    )
    response_data = [lesson.model_dump() for lesson in lesson_list]

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.post(
    "/",
    response_model=LessonSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
async def create_lesson(
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    new_lesson: CreateLessonSchema,
) -> JSONResponse:
    """Создание урока"""
    logger.debug("create lesson")
    created_lesson = await lesson_service.create_lesson(new_lesson)
    response_data = created_lesson.model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.get(
    "/stats",
    response_model=List[LessonSchema],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=100)
async def get_lessons_list_with_stats(
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
) -> JSONResponse:
    """Получение списка уроков c шагами и со статистикой"""
    logger.debug("get_lessons_list with stats}")
    lesson_list = await lesson_service.get_all_lessons_with_steps_and_stats()
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
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
    id: int,
) -> JSONResponse:
    """Получение урока по id"""
    logger.debug("get_lesson_by_id user_id={user_id}")
    lesson = await lesson_service.get_one_lesson_with_steps(
        user_id=user_id,
        lesson_id=id,
    )
    response_data = LessonSchema.model_validate(lesson).model_dump()
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
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    id: int,
    step_id: int,
) -> JSONResponse:
    """Получение этапа урока по id"""
    logger.debug(f"get_lesson_step_by_id lesson_id={id} step_id={step_id} ")

    step = await lesson_service.get_lesson_step_with_texts(
        step_id=step_id,
    )
    response_data = LessonStepSchema.model_validate(step).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.post(
    "/{id}/steps",
    response_model=LessonStepSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    dependencies=[Depends(users_deps.is_auth_dep)],
)
async def create_lesson_step(
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    id: int,
    step_id: int,
    new_step: CreateLessonStepForm,
) -> JSONResponse:
    """Создание этапа крока"""
    logger.debug(f"get_lesson_step_by_id lesson_id={id} step_id={step_id} ")

    new_step.lesson_id = id

    created_step = await lesson_service.create_lesson_step(
        new_step=CreateLessonStepForm.model_validate(new_step)
    )

    response_data = LessonStepSchema.model_validate(created_step).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.post(
    "/{id}/steps/{step_id}/result",
    response_model=DbEntityBaseSchema,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    dependencies=[Depends(users_deps.is_auth_dep)],
)
async def set_lesson_step_result(
    lesson_service: Annotated[
        LessonsService,
        Depends(lessons_deps.get_lesson_service_dep),
    ],
    user_id: Annotated[
        int,
        Depends(users_deps.get_current_user_id_dep),
    ],
    id: int,
    step_id: int,
    new_step_result: SetLessonStepResultForm,
) -> JSONResponse:
    """Создание или обновление результа урока"""
    logger.debug(f"get_lesson_step_by_id lesson_id={id} step_id={step_id} ")

    step_id = await lesson_service.set_lesson_step_result(
        step_id=step_id,
        new_step_result=new_step_result,
        user_id=user_id,
    )
    response_data = DbEntityBaseSchema.model_validate({"id": step_id}).model_dump()

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
