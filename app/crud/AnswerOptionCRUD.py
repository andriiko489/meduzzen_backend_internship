from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models
from schemas import quiz_schemas

default_session = session


class AnswerOptionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.AnswerOption, schema=quiz_schemas.BasicAnswerOption):
        super().__init__(session, model, schema)

    async def add(self, answer_option: quiz_schemas.BasicAnswerOption):
        return await super().add(answer_option)


answer_option_crud = AnswerOptionCRUD()
