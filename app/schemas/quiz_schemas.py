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

    @model_validator(mode='after')
    async def check_questions(self):
        questions = await question_crud.get_by_quiz_id(self.id)
        if len(questions) < 2:
            return ValueError("Quiz must be have at least two questions")
        return self


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
    correct_answer: int

    quiz_id: Optional[int] = None

    @model_validator(mode='after')
    async def check_answer_options(self):
        answer_options = await answer_option_crud.get_by_question_id(self.id)
        if len(answer_options) < 2:
            return ValueError("Question must be have at least two answer option")
        return self


class BasicQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    correct_answer: int

    quiz_id: Optional[int] = None


class UpdateQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None

    text: str
    correct_answer: int


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
