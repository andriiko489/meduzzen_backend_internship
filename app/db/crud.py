from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import models, schemas


async def get_users(session: AsyncSession) -> list[models.User]:
    result = await session.execute(select(models.User))
    return result.scalars().all()


async def get_user(session: AsyncSession, id: int) -> models.User:
    results = await session.execute(f"SELECT * FROM users WHERE id={id}")
    return results.first()

async def add_user(session: AsyncSession, user: schemas.User) -> list[models.User]:
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.hashed_password)
    await session.commit()
    await session.refresh(db_user)
    result = await session.execute(select(models.User))
    return result.scalars().all()
