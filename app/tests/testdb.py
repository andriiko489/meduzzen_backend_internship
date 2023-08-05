from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from crud.AdminCRUD import AdminCRUD
from crud.AnswerOptionCRUD import AnswerOptionCRUD
from crud.CompanyCRUD import CompanyCRUD
from crud.InvitationCRUD import InvitationCRUD
from crud.QuestionCRUD import QuestionCRUD
from crud.QuizCRUD import QuizCRUD
from crud.UserCRUD import UserCRUD
from utils.config import settings


test_engine = create_async_engine(settings.test_database_url, echo=True)
test_session = AsyncSession(test_engine)

user_crud_test = UserCRUD(test_session)
company_crud_test = CompanyCRUD(test_session)
invitation_crud_test = InvitationCRUD(test_session)
admin_crud_test = AdminCRUD(test_session)
quiz_crud_test = QuizCRUD(test_session)
question_crud_test = QuestionCRUD(test_session)
answer_option_crud_test = AnswerOptionCRUD(test_session)
