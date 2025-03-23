from typing import ClassVar, List

from pydantic import BaseModel as BasePydanticModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.errors import ResourceNotFoundError
from src.database.base_model import BaseSqlAlchemyModel


class RepoTypeCheckedMeta(type):
    """Meta class для проверки правильности создания репозиториев"""

    def __new__(cls, clsname, bases, attrs):

        required_class_vars = {
            "model": BaseSqlAlchemyModel,
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

    model: ClassVar[type[BaseSqlAlchemyModel]] = BaseSqlAlchemyModel
    entity_schema: ClassVar[type[BasePydanticModel]] = BasePydanticModel
    create_schema: ClassVar[type[BasePydanticModel]] = BasePydanticModel
    update_schema: ClassVar[type[BasePydanticModel]] = BasePydanticModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> BasePydanticModel:
        """Получение объекта по id"""
        obj = await self.session.get(self.model, id)
        if obj is None:
            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            return self.entity_schema.model_validate(obj)

    async def get_all(self) -> List[BasePydanticModel]:
        """Получение всех объектов"""
        stmt = select(self.model)
        query_result = await self.session.execute(stmt)

        result = [
            self.entity_schema.model_validate(model)
            for model in query_result.scalars().all()
        ]
        return result

    async def add_one(self, new_entity: BasePydanticModel) -> BasePydanticModel:
        """Добавление объекта"""
        new_object = self.model(**new_entity.model_dump())
        self.session.add(new_object)
        await self.session.commit()
        return self.entity_schema.model_validate(new_object)

    async def update_one(
        self, id: int, update_entity: BasePydanticModel
    ) -> BasePydanticModel:
        """Обновление объекта"""
        query_result = await self.session.get(self.model, id)
        if query_result is None:
            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            for name, value in update_entity.model_dump().items():
                setattr(query_result, name, value)
            await self.session.commit()

            return self.entity_schema.model_validate(query_result)

    async def delete_one(self, id: int) -> int:
        """Удаление объекта"""
        query_result = await self.session.get(self.model, id)
        await self.session.commit()
        if query_result is None:
            raise ResourceNotFoundError(
                (
                    f"Not fond {self.model.__class__.__name__}\
                                          with id={id} was not found!"
                )
            )
        else:
            await self.session.delete(query_result)
            await self.session.commit()
            return id

    async def filter_by_field(self, **kwargs) -> List[BasePydanticModel]:
        """Фильтр любому полю"""
        filters = []
        for key, value in kwargs.items():
            if value is not None:
                filters.append(getattr(self.model, key) == value)
        stmt = select(self.model).filter(*filters)
        query_result = await self.session.execute(stmt)
        result = [
            self.entity_schema.model_validate(model)
            for model in query_result.scalars().all()
        ]
        return list(result)
