from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models
from schemas import basic_schemas

default_session = session


class QuizCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Quiz, schema=basic_schemas.Quiz):
        super().__init__(session, model, schema)

    async def get(self, quiz_id: int):
        return await super().get(quiz_id)

    async def get_all(self):
        return await super().get_all()

    async def add(self, quiz: basic_schemas.Quiz):
        return await super().add(quiz)


quiz_crud = QuizCRUD()
