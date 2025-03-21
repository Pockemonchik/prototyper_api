from src.database.base_repository import BaseSqlAlchemyRepository
from src.lessons.models import LessonModel, LessonResultModel
from sqlalchemy import select


from src.lessons.schemas import CreateLessonSchema, LessonSchema, UpdateLessonSchema


class LessonsRepository(BaseSqlAlchemyRepository):
    model = LessonModel
    entity_schema = LessonSchema
    create_schema = CreateLessonSchema
    update_schema = UpdateLessonSchema

    async def get_lessons_with_user_results(self, user_id: int):
        """Получение всех уроков с результатами пользователя"""
        stmt = (
            select(self.model)
            .join(LessonResultModel, self.model.results)
            .where(LessonResultModel.user_id == user_id)
        )
        obj_list = await self.session.execute(stmt)
        await self.session.close()

        result = [l for l in obj_list.scalars().all()]
        print("get_lessons_with_user_results", result)
        return result
