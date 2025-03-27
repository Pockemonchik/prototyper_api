from typing import List

from src.lessons.repository import (
    LessonsRepository,
    LessonsStepRepository,
    LessonsStepResultRepository,
)
from src.lessons.schemas import (
    CreateLessonStepResultSchema,
    LessonResultSchema,
    LessonSchema,
    LessonStepResultSchema,
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

        lessons = await self.lessons_repo.get_all_lessons()
        if user_id:
            for lesson in lessons:
                lesson.result = await self.collect_lesson_stats_by_user(
                    lesson_id=lesson.id,
                    user_id=user_id,
                )

        return lessons

    async def collect_lesson_stats_by_user(
        self,
        user_id: int,
        lesson_id: int,
    ) -> LessonResultSchema:
        """Сбор статистики пользователя по уроку"""
        step_results: List[LessonStepResultSchema] = (
            await self.lesson_step_result_repo.get_results_by_user_ant_lesson_with_timings(
                user_id=user_id, lesson_id=lesson_id
            )
        )
        lesson = await self.get_one_lesson_with_steps(
            lesson_id=lesson_id, user_id=user_id
        )
        step_resuts_count = len(step_results)
        steps_count = len(lesson.steps)

        lesson_result = LessonResultSchema(lesson_id=lesson_id, user_id=user_id)
        lesson_result.percentage = (step_resuts_count / steps_count) * 100
        lesson_result.average_wpm = (
            sum([int(result.wpm) if result.wpm else 0 for result in step_results])
            / step_resuts_count
        )
        lesson_result.total_time_spent = sum(
            [sum(result.timing_list) for result in step_results]
        )
        lesson_result.total_time_best = sum(
            [min(result.timing_list) for result in step_results]
        )
        return lesson_result

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
