import string
import random

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas import user_schemas, basic_schemas, invitation_schemas, quiz_schemas

from tests.testdb import user_crud_test, company_crud_test, test_session, invitation_crud_test, admin_crud_test, \
    quiz_crud_test, question_crud_test
from sqlalchemy.sql import text as sa_text

client = TestClient(app)


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@pytest.mark.asyncio
async def test_crud():
    await test_session.execute(sa_text('''TRUNCATE TABLE users CASCADE''').execution_options(autocommit=True))

    test_string = get_random_string(length=8)
    user = user_schemas.User(username=test_string, hashed_password=test_string, email=test_string, is_active=True)
    db_user = await user_crud_test.add(user)
    assert user is not None
    assert db_user.username == test_string
    user_id = db_user.id

    assert user.username == test_string
    company = basic_schemas.Company(name="PEPSICO", owner_id=db_user.id)
    db_company = await company_crud_test.add(company)
    assert db_company is not None
    assert await company_crud_test.get_company(db_company.id)
    company_id = db_company.id
    assert await user_crud_test.set_company(company_id, user_id)

    test_string_2 = get_random_string(length=8)
    user_2 = user_schemas.User(username=test_string_2, hashed_password=test_string_2, email=test_string_2,
                               is_active=True)
    db_user_2 = await user_crud_test.add(user_2)
    assert user_2 is not None
    assert db_user_2.username == test_string_2
    user_2_id = db_user_2.id

    invitation = invitation_schemas.BasicInvitation(sender_id=user_id, receiver_id=user_2_id, company_id=company_id)
    db_invitation = await invitation_crud_test.add(invitation)
    assert db_invitation is not None
    assert await invitation_crud_test.get(db_invitation.id)
    invitation_id = db_invitation.id
    assert await invitation_crud_test.accept_invitation(invitation_id)
    assert (await user_crud_test.get_user(user_2_id)).company_id == company_id

    admin = basic_schemas.BasicAdmin(company_id=company_id, user_id=user_2_id)
    db_admin = await admin_crud_test.set_admin(admin)
    assert db_admin is not None

    quiz = quiz_schemas.BasicQuiz(company_id=company_id,
                                  name=test_string,
                                  description=test_string,
                                  frequency=3)
    db_quiz = await quiz_crud_test.add(quiz)
    assert db_quiz is not None
    quiz_id = db_quiz.id
    db_quiz = await quiz_crud_test.get(quiz_id)
    assert db_quiz is not None

    question = quiz_schemas.BasicQuestion(quiz_id=quiz_id,
                                          text=test_string,
                                          correct_answer_id=1)
    db_question = await question_crud_test.add(question)
    assert db_question is not None
    question_id = db_question.id
    db_question = await question_crud_test.get(question_id)
    assert db_question is not None

    question_2 = quiz_schemas.BasicQuestion(quiz_id=quiz_id,
                                            text=test_string_2,
                                            correct_answer_id=1)
    db_question_2 = await question_crud_test.add(question_2)
    assert db_question_2 is not None
    question_2_id = db_question_2.id
    db_question_2 = await question_crud_test.get(question_2_id)
    assert db_question_2 is not None
