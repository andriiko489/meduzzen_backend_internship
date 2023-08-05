from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from crud.AnswerOptionCRUD import answer_option_crud
from crud.QuestionCRUD import question_crud


class Quiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    name: str
    description: str
    frequency: int

    company_id: Optional[int] = None


class BasicQuiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    frequency: int

    company_id: int


class UpdateQuiz(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    name: str
    description: str
    frequency: int


class Question(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str
    correct_answer_id: int

    quiz_id: Optional[int] = None


class BasicQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    correct_answer_id: int

    quiz_id: Optional[int] = None


class UpdateQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str
    correct_answer_id: int


class AnswerOption(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str

    question_id: Optional[int] = None


class BasicAnswerOption(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str

    question_id: Optional[int] = None


class UpdateAnswerOption(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str
