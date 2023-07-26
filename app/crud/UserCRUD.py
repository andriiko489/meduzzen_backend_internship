from typing import Optional

from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db import pgdb
from schemas import models, schemas
from services.hasher import Hasher


default_session = pgdb.session


class UserCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.User, schema=schemas.User):
        super().__init__(session, model, schema)

    async def get_user(self, user_id: int) -> Optional[models.User]:
        return await super().get(user_id)

    async def get_by_username(self, username: str) -> Optional[models.User]:
        stmt = select(self.model).where(self.model.username == username)
        item = (await self.session.execute(stmt)).scalars().first()
        return item

    async def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(self.model).where(self.model.email == email)
        item = (await self.session.execute(stmt)).scalars().first()
        return item

    async def get_users(self) -> list[models.User]:
        return await super().get_all()

    async def add(self, user: schemas.User) -> Optional[models.User]:
        self.schema = schemas.AddUser
        user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        return await super().add(user)

    async def update(self, user: schemas.UpdateUser) -> Optional[models.User]:
        self.schema = schemas.UpdateUser
        if user.hashed_password is not None:
            user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        await super().update(user)
        return await self.get(user.id)  # it needeed because UserUpdate have email = None

    async def delete(self, user_id: int) -> Optional[models.User]:
        return await super().delete(user_id)


user_crud = UserCRUD()
