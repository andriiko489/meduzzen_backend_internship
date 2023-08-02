from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models
from schemas import basic_schemas

default_session = session


class QuestionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Question, schema=basic_schemas.Question):
        super().__init__(session, model, schema)

    async def add(self, question: basic_schemas.Question):
        return await super().add(question)


question_crud = QuestionCRUD()
