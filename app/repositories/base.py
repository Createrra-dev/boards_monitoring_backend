import logging
from typing import Any, Sequence

from asyncpg import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import asc, desc, insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ObjectAlreadyexistsException, ObjectNotFoundException
from app.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(
        self,
        *filter,
        order_by: str | None = None,
        descending: bool = False,
        use_default_sort: bool = True,
        limit: int = None,
        offset: int = None,
        **filter_by,
    ) -> list[BaseModel | Any]:
        """Возвращает список объектов с применением фильтров и сортировки.

        Args:
            *filter: Позиционные фильтры SQLAlchemy (например, model.field == value).
            order_by (str | None): Название поля для сортировки.
            descending (bool): Если True, сортировка по убыванию.
            use_default_sort (bool): Если True и order_by не указан, сортирует по id.
            limit (int | None): Ограничение на количество возвращаемых записей.
            offset (int | None): Смещение для пагинации.
            **filter_by: Фильтры вида field=value.

        Returns:
            list[BaseModel | Any]: Список объектов, преобразованных через mapper.
        """
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        if order_by:
            column = getattr(self.model, order_by, None)
            if column is not None:
                query = query.order_by(desc(column) if descending else asc(column))
        elif use_default_sort and hasattr(self.model, "id"):
            query = query.order_by(asc(self.model.id))
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self, *args, **kwargs) -> Sequence[BaseModel | Any]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
            return self.mapper.map_to_domain_entity(result.scalar_one())
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные={data}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyexistsException from ex
            elif isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]):
        try:
            stmt = insert(self.model).values([entity.model_dump() for entity in data])
            await self.session.execute(stmt)
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД, входные данные={data}")
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex

    async def edit(
        self, data: BaseModel, exclude_unset, **filter_by
    ) -> BaseModel | Any:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by) -> BaseModel | Any:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def delete_bulk(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
