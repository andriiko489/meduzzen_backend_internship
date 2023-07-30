from fastapi import APIRouter

from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models import models
from schemas import user_schemas, token_schemas, basic_schemas
from crud.UserCRUD import user_crud
from services.auth import Auth
from utils.logger import logger
from utils.config import settings

router = APIRouter(
    prefix="/users",
    tags=["users"])


@router.get("/all/")
async def get_users(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    logger.info("Someone want list of all users")
    return await user_crud.get_users()


@router.get("/get", response_model=user_schemas.UserResponse)
async def get_user(user_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    user = await user_crud.get_user(user_id=user_id)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    return user_schemas.UserResponse(msg="User found", user=user)


@router.post("/add", response_model=user_schemas.UserResponse)
async def add_user(user: user_schemas.AddUser):
    db_user: models.User = await user_crud.add(user=user)
    if not db_user:
        raise HTTPException(detail="User with this email or username already exist", status_code=418)
    return user_schemas.UserResponse(msg="Success", user=db_user)


@router.patch("/update", response_model=user_schemas.UserResponse)
async def update_user(user: user_schemas.UpdateUser, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    user = await user_crud.update(user=user)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    return user_schemas.UserResponse(msg="Success", user=user)


@router.delete("/delete", response_model=user_schemas.UserResponse)
async def delete_user(user_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(detail="User can delete only yourself", status_code=403)
    user = await user_crud.delete(user_id=user_id)
    return user_schemas.UserResponse(msg="Success", user=user)


@router.get("/owner_of")
async def get_owner_of(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await user_crud.get_by_owner_of(current_user.id)


@router.post("/token", response_model=token_schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user: models.User = await Auth.authenticate_user(form_data.username, form_data.password)
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
    return token_schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=user_schemas.User)
async def get_me(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return current_user
