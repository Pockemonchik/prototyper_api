from sqladmin import ModelView

from src.lessons.models import LessonModel


class LessonAdmin(ModelView, model=LessonModel):
    column_list = [LessonModel.id, LessonModel.name]
