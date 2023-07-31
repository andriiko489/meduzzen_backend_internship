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


admin_crud = AdminCRUD()