from sqlalchemy.ext.asyncio import AsyncSession

from crud.BaseCRUD import BaseCRUD
from schemas import models, schemas


class UserCRUD(BaseCRUD):
    def __init__(self, model=models.User, schema=schemas.User):
        super().__init__(model, schema)

    async def get_user(self, session: AsyncSession, user_id: int):
        return await super().get(session, user_id)

    async def get_users(self, session: AsyncSession):
        return await super().get_all(session)

    async def add(self, session: AsyncSession, user: schemas.User):
        self.schema = schemas.SignUpUser
        return await super().add(session, user)

    async def update(self, session: AsyncSession, user: schemas.UpdateUser):
        self.schema = schemas.UpdateUser
        return await super().update(session, user)

    async def delete(self, session: AsyncSession, user_id: int):
        return await super().delete(session, user_id)
