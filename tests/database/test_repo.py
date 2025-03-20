import pytest
from src.database.base_repository import BaseSqlAlchemyRepository

from pydantic import BaseModel as BasePydanticModel

from src.lessons.models import LessonModel
from src.lessons.schemas import LessonSchema


def test_cant_create_invalid_repo():

    with pytest.raises(ValueError):

        class TestRepo1(BaseSqlAlchemyRepository):
            pass

        assert not TestRepo1

    with pytest.raises(TypeError):

        class TestRepo2(BaseSqlAlchemyRepository):
            model = LessonModel
            entity_schema = LessonModel
            create_schema = BasePydanticModel
            update_schema = BasePydanticModel

        assert not TestRepo2


def test_can_create_repo():

    class TestRepo2(BaseSqlAlchemyRepository):
        model = LessonModel
        entity_schema = LessonSchema
        create_schema = LessonSchema
        update_schema = LessonSchema

    assert TestRepo2
