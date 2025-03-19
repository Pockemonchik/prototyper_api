from src.core.errors import ResourceNotFoundError
from src.lessons.models import LessonModel
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.lessons.shemas import CreateLessonSchema, LessonSchema, UpdateLessonSchema


class LessonsRepository:
    model = LessonModel

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int) -> LessonSchema:
        """Получение объекта по id"""
        obj = await self.session.get(self.model, id)
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise ResourceNotFoundError((f"Lesson with id={id} was not found!"))
        else:
            await self.session.close()
            return LessonSchema.model_validate(obj)

    async def get_all(self) -> List[LessonSchema]:
        """Получение всех объектов"""
        stmt = select(self.model)
        obj_list = await self.session.execute(stmt)
        await self.session.close()
        result = [LessonSchema.model_validate(l) for l in obj_list.scalars().all()]
        return result

    async def add_one(self, new_Lesson: CreateLessonSchema) -> LessonSchema:
        """Добавление объекта"""
        new_object = self.model(**new_Lesson.model_dump())
        self.session.add(new_object)
        await self.session.commit()
        await self.session.close()
        return LessonSchema.model_validate(new_object)

    async def update_one(
        self, id: int, Lesson_update: UpdateLessonSchema
    ) -> LessonSchema:
        """Обновление объекта"""
        obj = await self.session.get(self.model, id)
        if obj == None:
            await self.session.close()
            raise ResourceNotFoundError((f"Model with id={id} was not found!"))
        else:
            for name, value in Lesson_update.model_dump().items():
                setattr(obj, name, value)
            await self.session.commit()
            await self.session.close()
            return LessonSchema.model_validate(obj)

    async def delete_one(self, id: int) -> int:
        """Удаление объекта"""
        obj = await self.session.get(self.model, id)
        await self.session.commit()
        if obj == None:
            await self.session.close()
            raise ResourceNotFoundError((f"Lesson with id={id} was not found!"))
        else:
            await self.session.delete(obj)
            await self.session.commit()
            await self.session.close()
            return id

    async def filter_by_field(self, params: dict) -> List[LessonSchema]:
        """Фильтр любому полю"""
        filters = []
        for key, value in params.items():
            if value != None:
                filters.append(getattr(self.model, key) == value)
        stmt = select(self.model).filter(*filters)
        obj = await self.session.execute(stmt)
        await self.session.commit()
        result = [LessonSchema.model_validate(l) for l in obj.scalars().all()]
        return list(result)
