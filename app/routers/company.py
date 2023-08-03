from enum import Enum

from fastapi import APIRouter, HTTPException, Depends

from crud.AdminCRUD import admin_crud
from crud.CompanyCRUD import company_crud
from crud.UserCRUD import user_crud
from schemas import company_schemas, user_schemas, basic_schemas
from services.auth import Auth
from utils.logger import logger

router = APIRouter(
    prefix="/company",
    tags=["company"])


class ExceptionResponses(Enum):
    NOT_FOUND = "Company not found"
    ONLY_OWNER = "Only owner can do it"
    ONLY_OWNER_ADMIN = "Only owner and admins can do it"
    KICKED_TOO_HIGH = "Kicked user have too high role"
    NOT_MEMBER = "This user are not member of this company"


@router.get("/all/")
async def get_company(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    logger.info("Someone want list of all companies")
    return await company_crud.get_companies()


@router.get("/get")
async def get_companies(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id=company_id)
    if not company:
        raise HTTPException(detail=ExceptionResponses.NOT_FOUND.value, status_code=404)
    return company


@router.get("/members")
async def get_members(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    members = await company_crud.get_members(company_id)
    return members


@router.post("/add")
async def add_company(company: company_schemas.AddCompany,
                      current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = basic_schemas.Company(**company.model_dump())
    current_user_id = current_user.id
    company.owner_id = current_user.id
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(status_code=418)
    await user_crud.set_company(company_id=company.id, user_id=current_user_id)
    return company


@router.patch("/update")
async def update_company(company: company_schemas.RequestUpdateCompany,
                         current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await user_crud.get_role(user_id=current_user.id, company_id=company.id)
    if role.value < 2:
        raise HTTPException(detail=ExceptionResponses.ONLY_OWNER_ADMIN.value, status_code=403)
    company = company_schemas.UpdateCompany(**company.model_dump())
    company.owner_id = (await company_crud.get_company(company_id=company.id)).owner_id
    company = await company_crud.update(company=company)
    if not company:
        raise HTTPException(detail=ExceptionResponses.NOT_FOUND.value, status_code=404)
    return company


@router.delete("/kick_user")
async def kick_user(company_id: int, user_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id)
    if company is None:
        HTTPException(detail=ExceptionResponses.ONLY_OWNER.value, status_code=404)

    current_user_role = await user_crud.get_role(user_id=current_user.id, company_id=company_id)
    kicked_user_role = await user_crud.get_role(user_id=user_id, company_id=company_id)
    if kicked_user_role.value is None:
        HTTPException(detail=ExceptionResponses.NOT_FOUND.value, status_code=404)
    if kicked_user_role.value < 1:
        raise HTTPException(detail=ExceptionResponses.NOT_MEMBER.value, status_code=403)
    if current_user_role.value < 2:
        raise HTTPException(detail=ExceptionResponses.ONLY_OWNER_ADMIN.value, status_code=403)
    if current_user_role.value < kicked_user_role.value:
        raise HTTPException(detail=ExceptionResponses.KICKED_TOO_HIGH.value, status_code=403)
    if kicked_user_role.value > 1:
        admin = await admin_crud.get_by_user_id(user_id=user_id)
        admin_crud.delete(admin_id=admin.id)
    return await user_crud.set_company(None, user_id)


@router.delete("/delete_company")
async def delete_company(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id)
    if not company:
        HTTPException(detail=ExceptionResponses.NOT_FOUND.value, status_code=404)
    role = await user_crud.get_role(user_id=current_user.id, company_id=company.id)
    if role.value != 3:
        raise HTTPException(detail=ExceptionResponses.ONLY_OWNER.value, status_code=403)
    company = await company_crud.delete(company_id=company_id)
    return company
