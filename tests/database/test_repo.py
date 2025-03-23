import pytest
from pydantic import BaseModel as BasePydanticModel

from src.database.base_model import BaseSqlAlchemyModel
from src.database.base_repository import BaseSqlAlchemyRepository
from src.lessons.models import LessonModel
from src.lessons.schemas import LessonSchema


def test_cant_create_invalid_repo():

    with pytest.raises(ValueError):

        class TestRepo1(BaseSqlAlchemyRepository):
            pass

        assert TestRepo1.model is BaseSqlAlchemyModel

    with pytest.raises(TypeError):

        class TestRepo2(BaseSqlAlchemyRepository):
            model = LessonModel
            entity_schema = LessonModel  # type: ignore
            create_schema = BasePydanticModel
            update_schema = BasePydanticModel


def test_can_create_repo():

    class TestRepo2(BaseSqlAlchemyRepository):
        model = LessonModel
        entity_schema = LessonSchema
        create_schema = LessonSchema
        update_schema = LessonSchema

    assert TestRepo2.model is LessonModel
