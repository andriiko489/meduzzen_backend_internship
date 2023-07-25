import string
import random

import pytest
from fastapi.testclient import TestClient

from main import app
from schemas import schemas
from tests.connect_to_testdb import user_crud_test

client = TestClient(app)

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def test_main():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_crud():
    test_string = get_random_string(length=8)
    user = schemas.User(username=test_string, hashed_password=test_string, email=test_string, is_active=True)
    db_user = await user_crud_test.add(user)
    assert db_user.username == user.username
    assert await user_crud_test.get_user(db_user.id)
    assert await user_crud_test.delete(db_user.id)
