from fastapi import HTTPException
from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD, session
from schemas import models, schemas
from services.hasher import Hasher


class UserCRUD(BaseCRUD):
    def __init__(self, model=models.User, schema=schemas.User):
        super().__init__(model, schema)

    async def get_user(self, user_id: int):
        return await super().get(user_id)

    async def get_by_username(self, username: str):
        stmt = select(self.model).where(self.model.username == username)
        item = (await session.execute(stmt)).scalars().first()
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item
    async def get_users(self):
        return await super().get_all()

    async def add(self, user: schemas.User):
        self.schema = schemas.SignUpUser
        user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        return await super().add(user)

    async def update(self, user: schemas.UpdateUser):
        self.schema = schemas.UpdateUser
        if user.hashed_password is not None:
            user.hashed_password = Hasher.get_password_hash(user.hashed_password)
        return await super().update(user)

    async def delete(self, user_id: int):
        return await super().delete(user_id)


user_crud = UserCRUD()
