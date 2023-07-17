from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import models, schemas


async def get_users(session: AsyncSession) -> list[models.User]:
    result = await session.execute(select(models.User))
    return result.scalars().all()


async def get_user(session: AsyncSession, user_id: int) -> models.User:
    user = await session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def add_user(session: AsyncSession, user: schemas.User) -> list[models.User]:
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.hashed_password)
    await session.commit()
    await session.refresh(db_user)
    result = await session.execute(select(models.User))
    return result.scalars().all()


def return_if_not_empty(pd_field, db_field):
    if pd_field is not None:
        db_field = pd_field
    return db_field


async def update_user(session: AsyncSession, user: schemas.UpdateUser):
    db_user = await get_user(session, user.id)
    db_user.username = return_if_not_empty(user.username, db_user.username)
    db_user.hashed_password = return_if_not_empty(user.hashed_password, db_user.hashed_password)
    db_user.email = return_if_not_empty(user.email, db_user.email)
    await session.commit()
    await session.flush(db_user)
    return await get_user(session, user.id)


async def delete_user(session: AsyncSession, user_id: int):
    user = await get_user(session, user_id)
    await session.delete(user)
    await session.commit()
    return {"status": 202}
