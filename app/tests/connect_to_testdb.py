from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from crud.UserCRUD import UserCRUD
from utils.config import settings


test_engine = create_async_engine(settings.test_database_url, echo=True)
test_async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)
test_session = AsyncSession(test_engine)

user_crud_test = UserCRUD(test_session)
