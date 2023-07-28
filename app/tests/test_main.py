import string
import random

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas import user_schemas, company_schemas

from tests.connect_to_testdb import user_crud_test, company_crud_test, test_session
from sqlalchemy.sql import text as sa_text

client = TestClient(app)



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def test_main():
    response = client.get("/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_crud():
    await test_session.execute(sa_text('''TRUNCATE TABLE users CASCADE''').execution_options(autocommit=True))
    test_string = get_random_string(length=8)
    user = user_schemas.User(username=test_string, hashed_password=test_string, email=test_string, is_active=True)
    assert user is not None
    db_user = await user_crud_test.add(user)
    assert db_user.username == user.username
    assert await user_crud_test.get_user(db_user.id)
    assert await user_crud_test.delete(db_user.id)

    user = await user_crud_test.get_user(db_user.id)
    company = company_schemas.Company(name="PEPSICO", owner=user)
    db_company = await company_crud_test.add(company)
    assert db_company is not None
    assert await company_crud_test.get_company(db_company.id)
    assert await company_crud_test.delete(db_company.id)
