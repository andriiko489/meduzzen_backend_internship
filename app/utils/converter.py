from schemas import schemas


def to_pydantic(db_user):
    return schemas.User(hashed_password=db_user.hashed_password, username=db_user.username, email=db_user.email,
                        is_active=db_user.is_active)