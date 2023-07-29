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

    company_id: Mapped[Optional[int]] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="members", foreign_keys=[company_id])

    owner_model: Mapped["Owner"] = relationship(back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    members: Mapped[List["User"]] = relationship(back_populates="company")

    owner: Mapped["Owner"] = relationship(back_populates="company")


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="owner_model")

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped[List["Company"]] = relationship(back_populates="owner")
