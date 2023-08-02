from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models
from schemas import basic_schemas

default_session = session


class AnswerOptionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.AnswerOption, schema=basic_schemas.AnswerOption):
        super().__init__(session, model, schema)

    async def add(self, answer_option: basic_schemas.AnswerOption):
        return await super().add(answer_option)


answer_option_crud = AnswerOptionCRUD()
