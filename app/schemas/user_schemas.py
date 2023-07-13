from pydantic import BaseModel


class User(BaseModel):
    username: str
    hashed_password: str
    email: str


class SignInUser(BaseModel):
    username: str
    password: str


class SignUpUser(User):
    pass


class UserUpdate(BaseModel):
    username: str | None
    hashed_password: str | None
    email: str | None


class UserList(BaseModel):
    pass


class UserDetail(BaseModel):
    username: str
