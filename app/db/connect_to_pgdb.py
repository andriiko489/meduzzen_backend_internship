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
# INSERT INTO users (username, email, hashed_password, is_active) VALUES ('andriiko489', 'samplemail@gmail.com', 'hashed_password', True)
