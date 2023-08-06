from typing import List, Optional

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    owner_of: Mapped[Optional[List["Company"]]] = relationship(back_populates="owner",
                                                               foreign_keys="Company.owner_id")

    company_id: Mapped[Optional[int]] = mapped_column(ForeignKey("companies.id"))
    company: Mapped[Optional["Company"]] = relationship(back_populates="members",
                                                        foreign_keys=company_id)

    sent_invitations: Mapped[Optional[List["Invitation"]]] = relationship(back_populates="sender",
                                                                          foreign_keys="Invitation.sender_id",
                                                                          lazy="selectin")
    received_invitations: Mapped[Optional[List["Invitation"]]] = relationship(back_populates="receiver",
                                                                              foreign_keys="Invitation.receiver_id",
                                                                              lazy="selectin")
    admin_model: Mapped[Optional["Admin"]] = relationship(back_populates="user",
                                                          foreign_keys="Admin.user_id")

    progress_quizzes: Mapped[Optional["ProgressQuiz"]] = relationship(back_populates="user",
                                                                      foreign_keys="ProgressQuiz.user_id",
                                                                      lazy="selectin")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="owner_of",
                                         foreign_keys=owner_id,
                                         lazy="selectin")

    members: Mapped[List["User"]] = relationship(back_populates="company",
                                                 foreign_keys="User.company_id",
                                                 lazy="selectin")

    invitations: Mapped[List["Invitation"]] = relationship(back_populates="company",
                                                           foreign_keys="Invitation.company_id",
                                                           lazy="selectin")

    admins: Mapped[List["Admin"]] = relationship(back_populates="company",
                                                 foreign_keys="Admin.company_id",
                                                 lazy="selectin")

    quizzes: Mapped[List["Quiz"]] = relationship(back_populates="company",
                                                 foreign_keys="Quiz.company_id",
                                                 lazy="selectin")


class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True, index=True)

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sender: Mapped["User"] = relationship(back_populates="sent_invitations", foreign_keys=sender_id)

    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver: Mapped["User"] = relationship(back_populates="received_invitations", foreign_keys=receiver_id)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="invitations", foreign_keys=company_id)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="admin_model", foreign_keys=user_id)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="admins", foreign_keys=company_id)


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)
    frequency = Column(Integer)

    company_id: Mapped[Optional[int]] = mapped_column(ForeignKey("companies.id"))
    company: Mapped[Optional["Company"]] = relationship(back_populates="quizzes",
                                                        foreign_keys=company_id)

    questions: Mapped[List["Question"]] = relationship(back_populates="quiz",
                                                       foreign_keys="Question.quiz_id",
                                                       lazy="selectin")
    progress_quizzes: Mapped[Optional[List["ProgressQuiz"]]] = relationship(back_populates="quiz",
                                                                            foreign_keys="ProgressQuiz.quiz_id",
                                                                            lazy="selectin")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)

    text = Column(String)
    correct_answer_id = Column(Integer)

    quiz_id: Mapped[Optional[int]] = mapped_column(ForeignKey("quizzes.id"))
    quiz: Mapped[Optional["Quiz"]] = relationship(back_populates="questions",
                                                  foreign_keys=quiz_id)

    answer_options: Mapped[List["AnswerOption"]] = relationship(back_populates="question",
                                                                foreign_keys="AnswerOption.question_id",
                                                                lazy="selectin")

    answered_questions: Mapped[List["AnsweredQuestion"]] = relationship(back_populates="question",
                                                                        foreign_keys="AnsweredQuestion.question_id",
                                                                        lazy="selectin")


class AnswerOption(Base):
    __tablename__ = "answer_options"
    id = Column(Integer, primary_key=True, index=True)

    text = Column(String)

    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id"))
    question: Mapped[Optional["Question"]] = relationship(back_populates="answer_options",
                                                          foreign_keys=question_id)

    answered_questions: Mapped[List["AnsweredQuestion"]] = relationship(back_populates="answer",
                                                                        foreign_keys="AnsweredQuestion.answer_id",
                                                                        lazy="selectin")


class ProgressQuiz(Base):
    __tablename__ = "progress_quizzes"
    id = Column(Integer, primary_key=True, index=True)

    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    quiz: Mapped["Quiz"] = relationship(back_populates="progress_quizzes",
                                        foreign_keys=quiz_id)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="progress_quizzes",
                                        foreign_keys=user_id)

    answered_questions: Mapped[List["AnsweredQuestion"]] = relationship(back_populates="progress_quiz",
                                                                        foreign_keys="AnsweredQuestion.progress_quiz_id",
                                                                        lazy="selectin")


class AnsweredQuestion(Base):
    __tablename__ = "answered_questions"
    id = Column(Integer, primary_key=True, index=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    question: Mapped["Question"] = relationship(back_populates="answered_questions",
                                                foreign_keys=question_id)

    answer_id: Mapped[int] = mapped_column(ForeignKey("answer_options.id"))
    answer: Mapped["AnswerOption"] = relationship(back_populates="answered_questions",
                                                  foreign_keys=answer_id)

    progress_quiz_id: Mapped[int] = mapped_column(ForeignKey("progress_quizzes.id"))
    progress_quiz: Mapped["ProgressQuiz"] = relationship(back_populates="answered_questions",
                                                         foreign_keys=progress_quiz_id)
