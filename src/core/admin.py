from sqladmin import ModelView

from src.lessons.models import (
    LessonModel,
    LessonResultModel,
    LessonStepModel,
    LessonStepResultModel,
    LessonStepTextModel,
    LessonStepTimingModel,
)
from src.users.models import UserModel


class LessonModelAdmin(ModelView, model=LessonModel):
    column_list = [LessonModel.id, LessonModel.name]


class LessonResultModelAdmin(ModelView, model=LessonResultModel):
    column_list = [
        LessonResultModel.id,
        LessonResultModel.user_id,
        LessonResultModel.lesson_id,
    ]


class LessonStepModelAdmin(ModelView, model=LessonStepModel):
    column_list = [LessonStepModel.id, LessonStepModel.lesson_id]


class LessonStepTextModelAdmin(ModelView, model=LessonStepTextModel):
    column_list = [LessonStepTextModel.id]


class LessonStepResultModelAdmin(ModelView, model=LessonStepResultModel):
    column_list = [
        LessonStepResultModel.id,
        LessonStepResultModel.user_id,
        LessonStepResultModel.lesson_step_id,
    ]


class LessonStepTimingModelAdmin(ModelView, model=LessonStepTimingModel):
    column_list = [LessonStepTimingModel.id]


class UserModelAdmin(ModelView, model=UserModel):
    column_list = [UserModel.id, UserModel.username]
