import pytest
from fastapi.testclient import TestClient

from main import app
from crud.UserCRUD import user_crud_test
from schemas import schemas

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_crud():
    user = schemas.User(username="dsa", hashed_password="dsa", email="dsa", is_active=True)
    db_user = await user_crud_test.add(user)
    assert db_user.username == user.username
    assert await user_crud_test.get_user(db_user.id)
    assert await user_crud_test.delete(db_user.id)
