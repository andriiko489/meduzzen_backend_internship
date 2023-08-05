from crud.BaseCRUD import BaseCRUD
from db.pgdb import session
from models import models

default_session = session


class ProgressQuizCRUD(BaseCRUD):
    def __init__(self, session=default_session, model=models.ProgressQuiz):
        super().__init__(session, model)


progress_quiz_crud = ProgressQuizCRUD()
