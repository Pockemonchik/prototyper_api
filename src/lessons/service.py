from typing import List

from src.lessons.repository import (
    LessonsRepository,
    LessonsStepRepository,
    LessonsStepResultRepository,
    LessonsStepTimingRepository,
    LessonStepTextRepository,
)
from src.lessons.schemas import (
    CreateLessonSchema,
    CreateLessonStepForm,
    CreateLessonStepResultSchema,
    CreateLessonStepSchema,
    CreateLessonStepTextSchema,
    CreateLessonStepTimingSchema,
    LessonResultSchema,
    LessonSchema,
    LessonStatsSchema,
    LessonStepResultSchema,
    LessonStepSchema,
    LessonStepStatsSchema,
    SetLessonStepResultForm,
    UpdateLessonStepResultSchema,
)
from src.users.schemas import UserLessonsStats


class LessonsService:
    """Сервис управления уроками"""

    def __init__(
        self,
        lessons_repo: LessonsRepository,
        lesson_steps_repo: LessonsStepRepository,
        lesson_step_result_repo: LessonsStepResultRepository,
        lesson_step_timing_repo: LessonsStepTimingRepository,
        lesson_step_text_repo: LessonStepTextRepository,
    ):
        self.lessons_repo = lessons_repo
        self.lesson_steps_repo = lesson_steps_repo
        self.lesson_step_result_repo = lesson_step_result_repo
        self.lesson_step_timing_repo = lesson_step_timing_repo
        self.lesson_step_text_repo = lesson_step_text_repo

    async def create_lesson(self, new_lesson: CreateLessonSchema) -> LessonSchema:
        """Создание урока"""
        created_lesson = await self.lessons_repo.add_one(new_entity=new_lesson)

        return created_lesson

    async def create_lesson_step(
        self, new_step: CreateLessonStepForm
    ) -> LessonStepSchema:
        """Создание этапа урока с текстами"""
        new_step_valid = CreateLessonStepSchema.model_validate(new_step.model_dump())
        created_step = await self.lesson_steps_repo.add_one(new_entity=new_step_valid)
        for text in new_step.texts:
            new_text = CreateLessonStepTextSchema(
                lesson_step_id=created_step.id, text=text
            )
            await self.lesson_step_text_repo.add_one(new_text)
        return created_step

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

    async def get_all_lessons_with_steps_and_stats(self) -> List[LessonSchema]:
        """Получение всех уроков с шагами и статистикой"""
        lessons_id_list = [
            lesson.id for lesson in await self.lessons_repo.get_all_lessons()
        ]
        lessons = []
        for lesson_id in lessons_id_list:
            lesson: LessonSchema = await self.get_one_lesson_with_steps(
                lesson_id=lesson_id
            )
            lesson.stats = await self.get_lesson_stats(lesson_id=lesson.id)
            for step in lesson.steps:
                step.stats = await self.get_lesson_step_stats(lesson_step_id=step.id)
            lessons.append(lesson)

        return lessons

    async def get_user_lessons_stats(self, user_id: int) -> UserLessonsStats:
        """Общая статистика пользователя по прохождению уроков"""
        lessons = await self.get_all_lessons_with_user_results(user_id=user_id)
        user_stats = UserLessonsStats()
        user_stats.completed_lessons_count = len(
            [
                lesson.result.percentage
                for lesson in lessons
                if lesson.result and lesson.result.percentage == 100
            ]
        )
        user_stats.lessons_count = len(
            [lesson.result for lesson in lessons if lesson.result]
        )

        user_stats.total_time_spent = sum(
            [
                lesson.result.total_time_spent
                for lesson in lessons
                if lesson.result and lesson.result.total_time_spent
            ]
        )

        return user_stats

    async def get_lesson_stats(self, lesson_id: int) -> LessonStatsSchema:
        """Общая статистика по уроку"""
        lesson: LessonSchema = await self.get_one_lesson_with_steps(lesson_id=lesson_id)
        stats = LessonStatsSchema()
        stats.steps_count = len(lesson.steps)
        all_users = []
        if lesson.steps:
            for step in lesson.steps:
                user_id_list = await self.lesson_step_result_repo.get_users_with_lesson_step_result(
                    step_id=step.id
                )
                all_users.extend(user_id_list)
        stats.users_count = len(set(all_users))

        return stats

    async def get_lesson_step_stats(self, lesson_step_id: int) -> LessonStepStatsSchema:
        """Общая статистика по шагу урока"""

        stats = LessonStepStatsSchema()
        user_id_list = (
            await self.lesson_step_result_repo.get_users_with_lesson_step_result(
                step_id=lesson_step_id
            )
        )
        stats.users_count = len(set(user_id_list))

        return stats

    async def get_one_lesson_with_steps(
        self, lesson_id: int, user_id: int | None = None
    ) -> LessonSchema:
        """Получение урока с этапами и их результатми"""
        lesson = await self.lessons_repo.get_one_lesson_with_steps(
            user_id=user_id,
            lesson_id=lesson_id,
        )
        if user_id:
            lesson.result = await self.collect_lesson_stats_by_user(
                user_id=user_id,
                lesson_id=lesson_id,
            )
        return lesson

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
        lesson = await self.lessons_repo.get_one_lesson_with_steps(
            lesson_id=lesson_id, user_id=user_id
        )
        step_results_count = len(step_results) if lesson.steps else 0
        steps_count = len(lesson.steps) if lesson.steps else 0
        lesson_result = LessonResultSchema(lesson_id=lesson_id, user_id=user_id)

        if step_results_count and steps_count:
            lesson_result.percentage = int((step_results_count / steps_count) * 100)
            lesson_result.average_wpm = int(
                sum([int(result.wpm) if result.wpm else 0 for result in step_results])
                / step_results_count
            )
            lesson_result.total_time_spent = sum(
                [
                    sum(result.timing_list)
                    for result in step_results
                    if result.timing_list
                ]
            )
            lesson_result.total_time_best = sum(
                [
                    min(result.timing_list)
                    for result in step_results
                    if result.timing_list
                ]
            )
        return lesson_result

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
            # обновляем существующий результат
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

        else:
            # создаем новый результат
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
        # добавляем время к результату
        if new_step_result.timing:
            new_timing = CreateLessonStepTimingSchema(
                seconds=new_step_result.timing, lesson_step_result_id=result.id
            )
            await self.lesson_step_timing_repo.add_one(new_timing)

        return result.id
