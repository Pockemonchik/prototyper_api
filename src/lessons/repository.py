from typing import List
from src.core.errors import ResourceNotFoundError
from src.database.base_repository import BaseSqlAlchemyRepository
from src.lessons.models import (
    LessonModel,
    LessonResultModel,
    LessonStepModel,
    LessonStepResultModel,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload


from src.lessons.schemas import (
    CreateLessonSchema,
    CreateLessonStepSchema,
    LessonBaseSchema,
    LessonResultSchema,
    LessonSchema,
    LessonStepBaseSchema,
    LessonStepResultSchema,
    LessonStepSchema,
    UpdateLessonSchema,
    UpdateLessonStepSchema,
)


class LessonsRepository(BaseSqlAlchemyRepository):
    model = LessonModel
    entity_schema = LessonBaseSchema
    create_schema = CreateLessonSchema
    update_schema = UpdateLessonSchema

    async def get_all_lessons_with_user_results(
        self, user_id: int
    ) -> List[LessonSchema]:
        """Получение всех уроков с результатами пользователя"""
        if user_id:
            stmt = select(self.model).options(
                joinedload(
                    self.model.results.and_(LessonResultModel.user_id == user_id)
                )
            )
        else:
            stmt = select(self.model)
        obj_list = await self.session.execute(stmt)

        result = [
            LessonSchema.model_validate(
                {
                    **l.__dict__,
                    "result": (
                        LessonResultSchema.model_validate(l.results[0])
                        if user_id and l.results
                        else None
                    ),
                }
            )
            for l in obj_list.unique().scalars().all()
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
                    joinedload(
                        self.model.results.and_(LessonResultModel.user_id == user_id)
                    ),
                    joinedload(self.model.steps).joinedload(
                        LessonStepModel.results.and_(
                            LessonStepResultModel.user_id == user_id
                        )
                    ),
                )
                .where(self.model.id == lesson_id)
            )
        else:
            stmt = (
                select(self.model)
                .options(joinedload(self.model.steps))
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
                "result": (
                    LessonResultSchema.model_validate(lesson.results[0])
                    if user_id and lesson.results
                    else None
                ),
                "steps": [
                    LessonStepSchema.model_validate(
                        {
                            **step.__dict__,
                            "result": (
                                LessonStepResultSchema.model_validate(step.results[0])
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
    model = LessonStepModel
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
