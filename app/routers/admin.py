from fastapi import APIRouter, Depends, HTTPException

from crud.AdminCRUD import admin_crud
from crud.CompanyCRUD import company_crud
from crud.UserCRUD import user_crud
from schemas import user_schemas, basic_schemas
from services.auth import Auth

router = APIRouter(
    prefix="/admin",
    tags=["admin"])


@router.get("/all/")
async def get_admins(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await admin_crud.get_all()


@router.get("/get")
async def get_admin(admin_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    return await admin_crud.get_company(admin_id=admin_id)


@router.post("/set_admin")
async def set_admin(admin: basic_schemas.BasicAdmin, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(admin.company_id)
    user = await user_crud.get_user(admin.user_id)
    if company.owner_id != current_user.company_id:
        raise HTTPException(detail="Only owner can add admin to company", status_code=403)
    if company.id != user.company_id:
        raise HTTPException(detail="Only member of company can be admin", status_code=403)
    return await admin_crud.set_admin(admin)
