from enum import Enum


class ExceptionResponses(Enum):
    USER_NOT_FOUND = "User not found"
    COMPANY_NOT_FOUND = "Company not found"
    QUIZ_NOT_FOUND = "Quiz not found"
    QUESTION_NOT_FOUND = "Question not found"
    ANSWER_OPTION_NOT_FOUND = "Answer option not found"
    ANSWER_NOT_FOUND = "Answer not found"

    ONLY_OWNER_ADMIN = "Only owner and admins can do it"
    ONLY_OWNER = "Only owner can do it"
    NOT_MEMBER = "This user are not member of this company"
    KICKED_TOO_HIGH = "Kicked user have too high role"
    USER_HAVENT_COMPANY = "User havent company"

    HAVENT_ANSWER = "This question haven't this answer option"
    HAVENT_QUESTION = "Started quiz haven't this question"
    QUIZ_MUST_HAVE_TWO_QUESTIONS = "Quiz must be have at least two questions"
    QUIZ_NOT_STARTED = "User dont start quiz yet"
    ALREADY_ANSWERED = "You already answered to this question"

    CANNOT_SAVE = "Cannot save answer, unexpected error"
    SOMETHING_WRONG = "Something went wrong"
