from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_session
from src.lessons.repository import (
    LessonStepTextRepository,
    LessonsRepository,
    LessonsStepRepository,
    LessonsStepResultRepository,
    LessonsStepTimingRepository,
)
from src.lessons.service import LessonsService


async def get_lesson_service_dep(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonsService:
    """Получение сервиса lessons"""
    lessons_repo = LessonsRepository(session=session)
    lesson_steps_repo = LessonsStepRepository(session=session)
    lesson_step_result_repo = LessonsStepResultRepository(session=session)
    lesson_step_timing_repo = LessonsStepTimingRepository(session=session)
    lesson_step_text_repo = LessonStepTextRepository(session=session)
    service = LessonsService(
        lessons_repo=lessons_repo,
        lesson_steps_repo=lesson_steps_repo,
        lesson_step_result_repo=lesson_step_result_repo,
        lesson_step_timing_repo=lesson_step_timing_repo,
        lesson_step_text_repo=lesson_step_text_repo,
    )
    return service
