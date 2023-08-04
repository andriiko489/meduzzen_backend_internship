from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class AnswerOptionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.AnswerOption):
        super().__init__(session, model)

    async def add(self, answer_option):
        return await super().add(answer_option)

    async def get_by_question_id(self, question_id: int):
        stmt = select(models.AnswerOption).where(models.AnswerOption.question_id == question_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items


answer_option_crud = AnswerOptionCRUD()
