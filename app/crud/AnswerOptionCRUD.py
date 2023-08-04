from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class AnswerOptionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.AnswerOption):
        super().__init__(session, model)

    async def add(self, answer_option):
        return await super().add(answer_option)


answer_option_crud = AnswerOptionCRUD()
