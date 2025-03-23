from typing import List

from src.lessons.repository import (
    LessonsRepository,
    LessonsStepRepository,
    LessonsStepResultRepository,
)
from src.lessons.schemas import (
    CreateLessonStepResultSchema,
    LessonSchema,
    LessonStepSchema,
    SetLessonStepResultForm,
    UpdateLessonStepResultSchema,
)


class LessonsService:
    """Сервис управления уроками"""

    def __init__(
        self,
        lessons_repo: LessonsRepository,
        lesson_steps_repo: LessonsStepRepository,
        lesson_step_result_repo: LessonsStepResultRepository,
    ):
        self.lessons_repo = lessons_repo
        self.lesson_steps_repo = lesson_steps_repo
        self.lesson_step_result_repo = lesson_step_result_repo

    async def get_all_lessons_with_user_results(
        self, user_id: int | None
    ) -> List[LessonSchema]:
        """Получение всех уроков
        (с результатами пользователя если он авторизован)"""
        if user_id:

            result = await self.lessons_repo.get_all_lessons_with_user_results(
                user_id=user_id,
            )
        else:
            result = await self.lessons_repo.get_all_lessons()
        return result

    async def get_one_lesson_with_steps(
        self, lesson_id: int, user_id: int | None
    ) -> LessonSchema:
        """Получение урока с этапами и их результатми"""
        result = await self.lessons_repo.get_one_lesson_with_steps(
            user_id=user_id,
            lesson_id=lesson_id,
        )
        return result

    async def get_lesson_step_with_texts(
        self,
        step_id: int,
    ) -> LessonStepSchema:
        """Получение урока этапа урока по id"""
        result = await self.lesson_steps_repo.get_lesson_step_with_texts(
            step_id=step_id,
        )
        return result

    async def set_lesson_step_result(
        self, user_id: int, step_id: int, new_step_result: SetLessonStepResultForm
    ) -> int:
        """Обновление или создание нового результата по уроку"""

        exist_result = await self.lesson_step_result_repo.filter_by_field(
            lesson_step_id=step_id, user_id=user_id
        )
        if exist_result:
            updated_result = UpdateLessonStepResultSchema.model_validate(
                {
                    **new_step_result.model_dump(),
                    "user_id": user_id,
                    "lesson_step_id": step_id,
                }
            )
            result = await self.lesson_step_result_repo.update_one(
                id=exist_result[0].id, update_entity=updated_result
            )
            return result.id
        else:
            create_result = CreateLessonStepResultSchema.model_validate(
                {
                    **new_step_result.model_dump(),
                    "user_id": user_id,
                    "lesson_step_id": step_id,
                }
            )
            result = await self.lesson_step_result_repo.add_one(
                new_entity=create_result
            )
            return result.id
