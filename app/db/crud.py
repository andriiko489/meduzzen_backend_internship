from sqlalchemy.orm import Session

from schemas import models, schemas


def get_users(db: Session):
    return db.query(models.User).all()

def sign_up_user(db: Session, user: schemas.SignUpUser):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user