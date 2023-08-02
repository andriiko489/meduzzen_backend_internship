from enum import IntEnum
from typing import Optional

from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from crud.CompanyCRUD import CompanyCRUD
from db import pgdb
from models import models
from schemas import user_schemas, basic_schemas
from services.hasher import Hasher

default_session = pgdb.session


class Role(IntEnum):
    ANOTHER_COMPANY = -1
    UNEMPLOYED = 0
    MEMBER = 1
    ADMIN = 2
    OWNER = 3


class UserCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.User, schema=user_schemas.User):
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

    async def get_by_owner_of(self, owner_id: int):
        stmt = select(models.Company).where(models.Company.owner_id == owner_id)
        item = (await self.session.execute(stmt)).scalars().all()
        return item

    async def add(self, user: basic_schemas.User) -> Optional[models.User]:
        self.schema = user_schemas.AddUser
        user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        return await super().add(user)

    async def update(self, user: user_schemas.UpdateUser) -> Optional[models.User]:
        self.schema = user_schemas.UpdateUser
        if user.hashed_password is not None:
            user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        await super().update(user)
        return await self.get(user.id)  # it needeed because UserUpdate have email = None

    async def set_company(self, company_id: int, user_id: int):
        db_user = await self.get_user(user_id)
        db_user.company_id = company_id
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def delete(self, user_id: int) -> Optional[models.User]:
        return await super().delete(user_id)

    async def get_role(self, user_id: int, company_id: int):
        company_crud = CompanyCRUD(self.session)
        user_crud = UserCRUD(self.session)
        company = await company_crud.get_company(company_id)
        user = await user_crud.get_user(user_id)
        if not company:
            return None
        if not user:
            return None
        if user.company_id is None:
            return Role.UNEMPLOYED  # user
        if company.id != user.company_id:
            return Role.ANOTHER_COMPANY
        if company.owner_id == user_id:
            return Role.OWNER  # owner
        admins = await company_crud.get_admins(company.id)
        for admin in admins:
            if admin.user_id == user_id:
                return Role.ADMIN  # admin
        return Role.MEMBER


user_crud = UserCRUD()
