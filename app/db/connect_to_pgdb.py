from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from utils.config import settings

engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

test_engine = create_async_engine(settings.test_database_url, echo=True)
test_async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)
