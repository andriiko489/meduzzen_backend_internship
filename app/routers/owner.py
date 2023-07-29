from fastapi import APIRouter, Depends

from crud.OwnerCRUD import owner_crud
from schemas import user_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/owners",
    tags=["owners"])


@router.get("/all/")
async def get_users(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await owner_crud.get_all()
