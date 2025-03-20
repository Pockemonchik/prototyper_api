from src.database.base_repository import BaseSqlAlchemyRepository
from src.lessons.models import LessonModel


from src.lessons.schemas import CreateLessonSchema, LessonSchema, UpdateLessonSchema


class LessonsRepository(BaseSqlAlchemyRepository):
    model = LessonModel
    entity_schema = LessonSchema
    create_schema = CreateLessonSchema
    update_schema = UpdateLessonSchema
