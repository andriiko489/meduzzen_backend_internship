from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from crud.CompanyCRUD import CompanyCRUD
from crud.InvitationCRUD import InvitationCRUD
from crud.UserCRUD import UserCRUD
from utils.config import settings


test_engine = create_async_engine(settings.test_database_url, echo=True)
test_session = AsyncSession(test_engine)

user_crud_test = UserCRUD(test_session)
company_crud_test = CompanyCRUD(test_session)
invitation_crud_test = InvitationCRUD(test_session)