from src.core.errors import ResourceNotFoundError
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.database.base_model import BaseSqlAchemyModel
from typing import List

from pydantic import BaseModel as BasePydanticModel


class RepoTypeCheckedMeta(type):
    """Meta class для проверки правильности создания репозиториев"""

    def __new__(cls, clsname, bases, attrs):

        required_class_vars = {
            "model": BaseSqlAchemyModel,
            "entity_schema": BasePydanticModel,
            "create_schema": BasePydanticModel,
            "update_schema": BasePydanticModel,
        }
        for var in required_class_vars:
            if var not in attrs:
                raise ValueError(
                    " ".join(
                        [
                            "Class var not found!",
                            f"You must define class variable '{var}'",
                            f"with type {required_class_vars[var]}!",
                        ]
                    )
                )

            if var in attrs and (not issubclass(attrs[var], required_class_vars[var])):
                raise TypeError(
                    " ".join(
                        [
                            "Type of class class var not correct!",
                            f"You must define class variable '{var}'",
                            f"with type {required_class_vars[var]}!",
                        ]
                    )
                )

        return super().__new__(cls, clsname, bases, attrs)


class BaseSqlAlchemyRepository(metaclass=RepoTypeCheckedMeta):
    """Базовый класс для crud операций sqlalchemy"""

    model = BaseSqlAchemyModel
    entity_schema = BasePydanticModel
    create_schema = BasePydanticModel
    update_schema = BasePydanticModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> entity_schema:
        """Получение объекта по id"""
        obj = await self.session.get(self.model, id)
        if obj == None:

            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            return self.entity_schema.model_validate(obj)

    async def get_all(self) -> List[entity_schema]:
        """Получение всех объектов"""
        stmt = select(self.model)
        obj_list = await self.session.execute(stmt)

        result = [
            self.entity_schema.model_validate(l) for l in obj_list.scalars().all()
        ]
        return result

    async def add_one(self, new_entity: create_schema) -> entity_schema:
        """Добавление объекта"""
        new_object = self.model(**new_entity.model_dump())
        self.session.add(new_object)
        await self.session.commit()
        return self.entity_schema.model_validate(new_object)

    async def update_one(self, id: int, update_entity: update_schema) -> entity_schema:
        """Обновление объекта"""
        obj = await self.session.get(self.model, id)
        if obj == None:

            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            for name, value in update_entity.model_dump().items():
                setattr(obj, name, value)
            await self.session.commit()

            return self.entity_schema.model_validate(obj)

    async def delete_one(self, id: int) -> int:
        """Удаление объекта"""
        obj = await self.session.get(self.model, id)
        await self.session.commit()
        if obj == None:

            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            await self.session.delete(obj)
            await self.session.commit()

            return id

    async def filter_by_field(self, **kwargs) -> List[entity_schema]:
        """Фильтр любому полю"""
        filters = []
        for key, value in kwargs.items():
            if value != None:
                filters.append(getattr(self.model, key) == value)
        stmt = select(self.model).filter(*filters)
        obj = await self.session.execute(stmt)
        result = [self.entity_schema.model_validate(l) for l in obj.scalars().all()]
        return list(result)
