from sqladmin import ModelView

from src.lessons.models import LessonModel
from src.users.models import UserModel


class LessonAdmin(ModelView, model=LessonModel):
    column_list = [LessonModel.id, LessonModel.name]


class UserAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.username]
