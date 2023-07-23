from fastapi import APIRouter

from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import schemas
from crud.UserCRUD import user_crud
from schemas.schemas import SignUpUser, Token, UserResponse, UpdateUser
from services.auth import Auth
from utils.logger import logger
from utils.config import settings

router = APIRouter(
    prefix="/users",
    tags=["users"])



@router.get("/all/")
async def get_users() -> list[schemas.DbUser]:
    logger.info("Someone want list of all users")
    return await user_crud.get_users()


@router.get("/get", response_model=UserResponse)
async def get_user(user_id: int):
    user = await user_crud.get_user(user_id=user_id)
    if not user:
        return UserResponse(status_code=404, msg="User not found")
    return UserResponse(status_code=200, msg="User found", user=user)


@router.post("/add", response_model=UserResponse)
async def sign_up_user(user: SignUpUser):
    try:
        user = await user_crud.add(user=user)
        if user:
            return UserResponse(user=user, status_code=200, msg="Success")
        else:
            raise Exception("User with this email or username already exist, try again")
    except Exception as e:
        return UserResponse(status_code=404, msg=f"Error: {e}")


@router.patch("/update", response_model=UserResponse)
async def update_user(user: UpdateUser):
    user = await user_crud.update(user=user)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    return UserResponse(msg="Success", status_code=200, user=user)


@router.delete("/delete", response_model=UserResponse)
async def delete_user(user_id: int):
    user = await user_crud.delete(user_id=user_id)
    if not user:
        return UserResponse(msg="Unexpected error", status_code=404)
    return UserResponse(msg="Success", status_code=200, user=user)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await Auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = Auth.create_access_token(
        data={"sub": user.username, ".email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: schemas.User = Depends(Auth.get_current_user)):
    return current_user
