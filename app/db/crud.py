from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import TypeVar, Generic

T = TypeVar('T')


def return_if_not_empty(pd_field, db_field):
    if pd_field is not None:
        db_field = pd_field
    return db_field


class BaseCRUD(Generic[T]):
    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def get_columns(self):
        columns = [str(column) for column in self.model.__table__.columns]
        columns = [column[column.index(".") + 1:] for column in columns]
        columns = [column for column in columns
                   if column != "id"]
        return columns

    async def get(self, session: AsyncSession, item_id: int):
        item = await session.get(self.model, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item

    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, session: AsyncSession, item):
        d = {}
        for column in self.get_columns():
            d[column] = eval(f"item.{column}")
        db_item = self.model(**d)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    async def update(self, session: AsyncSession, item):
        db_item = await self.get(session, item.id)

        columns = self.get_columns()

        for column in columns:
            exec(f"db_item.{column} = return_if_not_empty(item.{column}, db_item.{column})")

        await session.commit()
        await session.flush(db_item)
        return await self.get(session, item.id)

    async def delete(self, session: AsyncSession, id: int):
        item = await self.get(session, id)
        await session.delete(item)
        await session.commit()
        return {"status": 202}
