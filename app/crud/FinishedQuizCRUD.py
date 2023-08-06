from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class FinishedQuizCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.FinishedQuiz):
        super().__init__(session, model)


finished_quiz_crud = FinishedQuizCRUD()
