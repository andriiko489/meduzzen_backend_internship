from sqlalchemy import select

from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class ProgressQuizCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.ProgressQuiz):
        super().__init__(session, model)

    async def get_by_user_id(self, user_id: int):
        stmt = select(models.ProgressQuiz).where(models.ProgressQuiz.user_id == user_id)
        item = (await self.session.execute(stmt)).scalars().first()
        return item


progress_quiz_crud = ProgressQuizCRUD()
