from sqlalchemy import select

from typing import TypeVar, Generic

T = TypeVar('T')


def return_if_not_empty(pd_field, db_field):
    if pd_field is not None:
        db_field = pd_field
    return db_field


class BaseCRUD(Generic[T]):
    def __init__(self, session, model, schema):
        self.model = model
        self.schema = schema
        self.session = session

    def get_columns(self):
        columns = [str(column) for column in self.model.__table__.columns]
        columns = [column[column.index(".") + 1:] for column in columns]
        columns = [column for column in columns
                   if column != "id"]
        return columns

    async def get(self, item_id: int):
        item = await self.session.get(self.model, item_id)
        return item

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add(self, item):
        d = {}
        columns = type(item).__fields__.keys()
        for column in columns:
            d[column] = eval(f"item.{column}")
        db_item = self.model(**d)
        try:
            db_item = await self.session.merge(db_item)
            self.session.add(db_item)
            await self.session.commit()
            await self.session.refresh(db_item)
        except:
            await self.session.rollback()
            db_item = None
        return db_item

    async def update(self, item):
        db_item = await self.get(item.id)

        columns = self.get_columns()
        try:
            for column in columns:
                exec(f"db_item.{column} = return_if_not_empty(item.{column}, db_item.{column})")
            await self.session.commit()
            await self.session.refresh(db_item)
        except:
            await self.session.rollback()
            item = None
        return item

    async def delete(self, id: int):
        item = await self.get(id)
        try:
            await self.session.delete(item)
            await self.session.commit()
        except:
            await self.session.rollback()
            item = None
        return item
