from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class FinishedQuizCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.FinishedQuiz):
        super().__init__(session, model)

    async def get_by_user_id(self, user_id: int):
        stmt = select(models.FinishedQuiz).where(models.FinishedQuiz.user_id == user_id)
        items = (await self.session.execute(stmt)).scalars().all()
        return items


finished_quiz_crud = FinishedQuizCRUD()
