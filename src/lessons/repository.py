from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.core.errors import ResourceNotFoundError
from src.database.base_repository import BaseSqlAlchemyRepository
from src.lessons.models import (
    LessonModel,
    LessonStepModel,
    LessonStepResultModel,
    LessonStepTextModel,
    LessonStepTimingModel,
)
from src.lessons.schemas import (
    CreateLessonSchema,
    CreateLessonStepResultSchema,
    CreateLessonStepSchema,
    CreateLessonStepTextSchema,
    CreateLessonStepTimingSchema,
    LessonBaseSchema,
    LessonSchema,
    LessonStepBaseSchema,
    LessonStepResultSchema,
    LessonStepSchema,
    LessonStepTextSchema,
    LessonStepTimingSchema,
    UpdateLessonSchema,
    UpdateLessonStepResultSchema,
    UpdateLessonStepSchema,
    UpdateLessonStepTextSchema,
    UpdateLessonStepTimingSchema,
)


class LessonsRepository(BaseSqlAlchemyRepository):
    """Репозиторий для управления данными об уроках"""

    model: type[LessonModel] = LessonModel
    entity_schema = LessonBaseSchema
    create_schema = CreateLessonSchema
    update_schema = UpdateLessonSchema

    async def get_all_lessons(self) -> List[LessonSchema]:
        """Получение всех уроков"""

        stmt = select(self.model)
        obj_list = await self.session.execute(stmt)

        result = [
            LessonSchema.model_validate({**lesson.__dict__, "result": None})
            for lesson in obj_list.unique().scalars().all()
        ]

        return result

    async def get_one_lesson_with_steps(
        self, lesson_id: int, user_id: int | None
    ) -> LessonSchema:
        """Получение урока с этапами и их результатми"""
        if user_id:
            stmt = (
                select(self.model)
                .options(
                    joinedload(self.model.steps)
                    .joinedload(LessonStepModel.results)
                    .options(joinedload(LessonStepResultModel.timings)),
                    joinedload(self.model.steps).joinedload(LessonStepModel.texts),
                )
                .where(self.model.id == lesson_id)
            )
        else:
            stmt = (
                select(self.model)
                .options(joinedload(self.model.steps).joinedload(LessonStepModel.texts))
                .where(self.model.id == lesson_id)
            )

        obj_list = await self.session.execute(stmt)

        query_result = obj_list.unique().scalars().all()
        if query_result:
            lesson = query_result[0]
        else:
            raise ResourceNotFoundError("Lesson not found")

        result = LessonSchema.model_validate(
            {
                **lesson.__dict__,
                "result": None,
                "steps": [
                    LessonStepSchema.model_validate(
                        {
                            **step.__dict__,
                            "texts": [text.text for text in step.texts],
                            "result": (
                                LessonStepResultSchema.model_validate(
                                    {
                                        **step.results[0].__dict__,
                                        "timing_list": [
                                            timing.seconds
                                            for timing in step.results[0].timings
                                        ],
                                    }
                                )
                                if user_id and step.results
                                else None
                            ),
                        }
                    )
                    for step in lesson.steps
                ],
            }
        )

        return result


class LessonsStepRepository(BaseSqlAlchemyRepository):
    """Репозиторий для управления данными о шагах урока"""

    model: type[LessonStepModel] = LessonStepModel
    entity_schema = LessonStepBaseSchema
    create_schema = CreateLessonStepSchema
    update_schema = UpdateLessonStepSchema

    async def get_lesson_step_with_texts(self, step_id: int) -> LessonStepSchema:
        """Получение всех уроков с результатами пользователя"""
        stmt = (
            select(self.model)
            .options(joinedload(self.model.texts))
            .where(self.model.id == step_id)
        )
        obj_list = await self.session.execute(stmt)

        query_result = obj_list.unique().scalars().all()

        if query_result:
            step = query_result[0]
        else:
            raise ResourceNotFoundError("Lesson not found")

        result = LessonStepSchema.model_validate(
            {
                **step.__dict__,
                "texts": [text.text for text in step.texts],
            }
        )

        return result


class LessonsStepResultRepository(BaseSqlAlchemyRepository):
    """Репозиторий для управления данными о рузультатах шага урока"""

    model: type[LessonStepResultModel] = LessonStepResultModel
    entity_schema = LessonStepResultSchema
    create_schema = CreateLessonStepResultSchema
    update_schema = UpdateLessonStepResultSchema

    async def get_results_by_user_ant_lesson_with_timings(
        self,
        lesson_id: int,
        user_id: int,
    ) -> List[LessonStepResultSchema]:
        """Получение результатов по степу с таймингами"""
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.timings),
            )
            .where(self.model.lesson_step.and_(LessonStepModel.lesson_id == lesson_id))
            .where(self.model.user_id == user_id)
        )
        obj_list = await self.session.execute(stmt)

        query_result = obj_list.unique().scalars().all()

        result = [
            LessonStepResultSchema.model_validate(
                {
                    **result.__dict__,
                    "timing_list": [
                        timing.seconds if timing.seconds else None
                        for timing in result.timings
                    ] if result.timings else None,
                }
            )
            for result in query_result
        ]

        return result

    async def get_users_with_lesson_step_result(self, step_id: int) -> LessonStepSchema:
        """Получение всех пользователей, кто проходил шаг урока"""
        stmt = (
            select(self.model.user_id)
            .distinct()
            .where(self.model.lesson_step_id == step_id)
        )
        obj_list = await self.session.execute(stmt)

        query_result = obj_list.unique().scalars().all()
        result = [int(obj) for obj in query_result]
        return result


class LessonsStepTimingRepository(BaseSqlAlchemyRepository):
    """Репозиторий для управления времени шага урока"""

    model: type[LessonStepTimingModel] = LessonStepTimingModel
    entity_schema = LessonStepTimingSchema
    create_schema = CreateLessonStepTimingSchema
    update_schema = UpdateLessonStepTimingSchema


class LessonStepTextRepository(BaseSqlAlchemyRepository):
    """Репозиторий для управления текстами уроков"""

    model: type[LessonStepTextModel] = LessonStepTextModel
    entity_schema = LessonStepTextSchema
    create_schema = CreateLessonStepTextSchema
    update_schema = UpdateLessonStepTextSchema
