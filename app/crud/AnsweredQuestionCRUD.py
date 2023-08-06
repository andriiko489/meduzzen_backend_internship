from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class AnsweredQuestionCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.AnsweredQuestion):
        super().__init__(session, model)

    async def get_by_progress_quiz_id(self, progress_quiz_id: int):
        stmt = select(models.AnsweredQuestion).where(models.AnsweredQuestion.progress_quiz_id == progress_quiz_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items

    async def get_by_answer_id(self, answer_id: int):
        stmt = select(models.AnsweredQuestion).where(models.AnsweredQuestion.answer_id == answer_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items

    async def get_by_question_id(self, question_id: int):
        stmt = select(models.AnsweredQuestion).where(models.AnsweredQuestion.question_id == question_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items

    async def get_by_question_id_and_progress_quiz_id(self, question_id: int, progress_quiz_id: int):
        stmt = select(models.AnsweredQuestion).where(models.AnsweredQuestion.question_id == question_id)\
            .where(models.AnsweredQuestion.progress_quiz_id == progress_quiz_id)
        items = (await self.session.execute(stmt)).scalars().first()
        return items


answered_question_crud = AnsweredQuestionCRUD()
