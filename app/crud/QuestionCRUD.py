from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class QuestionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.Question):
        super().__init__(session, model)

    async def add(self, question):
        return await super().add(question)

    async def get_by_quiz_id(self, quiz_id: int):
        stmt = select(models.Question).where(models.Question.quiz_id == quiz_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items


question_crud = QuestionCRUD()
