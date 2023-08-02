from typing import Optional

from pydantic import BaseModel, ConfigDict


class Quiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    name: str
    description: str
    frequency: int

    company_id: int


class BasicQuiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    frequency: int

    company_id: int


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str

    quiz_id: Optional[int] = None


class BasicQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str

    quiz_id: Optional[int] = None


class AnswerOption(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str

    question_id: Optional[int] = None


class BasicAnswerOption(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str

    question_id: Optional[int] = None
