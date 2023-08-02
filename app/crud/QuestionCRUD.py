from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models
from schemas import quiz_schemas

default_session = session


class QuestionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Question, schema=quiz_schemas.Question):
        super().__init__(session, model, schema)

    async def add(self, question: quiz_schemas.Question):
        return await super().add(question)


question_crud = QuestionCRUD()
