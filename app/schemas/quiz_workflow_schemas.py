from typing import Optional

from pydantic import BaseModel


class BasicProgressQuiz(BaseModel):
    id: Optional[int] = None
    quiz_id: int
    user_id: int


class ProgressQuiz(BaseModel):
    id: Optional[int] = None
    quiz_id: int
    user_id: int


class BasicAnsweredQuestion(BaseModel):
    question_id: int
    answer_id: int
    progress_quiz_id: int


class AnsweredQuestion(BaseModel):
    id: Optional[int] = None
    question_id: int
    answer_id: int
    progress_quiz_id: int
