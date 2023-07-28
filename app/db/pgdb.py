from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from utils.config import settings

engine = create_async_engine(settings.database_url, echo=True)
session = AsyncSession(engine)
