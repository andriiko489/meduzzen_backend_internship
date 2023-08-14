import datetime
from typing import Optional

from pydantic import BaseModel


class BasicProgressQuiz(BaseModel):
    quiz_id: int
    user_id: int


class ProgressQuiz(BasicProgressQuiz):
    id: Optional[int] = None


class BasicAnsweredQuestion(BaseModel):
    question_id: int
    answer_id: int
    progress_quiz_id: int


class AnsweredQuestion(BasicAnsweredQuestion):
    id: Optional[int] = None


class BasicFinishedQuiz(BaseModel):
    id: Optional[int] = None

    num_of_questions: int
    num_of_correct_answers: int
    user_id: int
    time: datetime.timedelta
    quiz_id: int
