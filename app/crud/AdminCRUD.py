from typing import Optional

from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from models import models
from schemas import basic_schemas

default_session = pgdb.session


class AdminCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Admin, schema=basic_schemas.Admin):
        super().__init__(session, model, schema)

    async def get(self, admin_id: int):
        return await super().get(admin_id)

    async def get_all(self):
        return await super().get_all()

    async def set_admin(self, admin: basic_schemas.BasicAdmin):
        admin = basic_schemas.Admin(**admin.model_dump())
        return await super().add(admin)

    async def delete(self, admin_id: int) -> Optional[models.Admin]:
        return await super().delete(admin_id)

    async def get_by_user_id(self, user_id: int):
        stmt = select(self.model).where(self.model.user_id == user_id)
        item = (await self.session.execute(stmt)).scalars().first()
        return item


admin_crud = AdminCRUD()
