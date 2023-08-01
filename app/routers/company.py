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


@router.get("/all/")
async def get_company(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    logger.info("Someone want list of all companies")
    return await company_crud.get_companies()


@router.get("/get")
async def get_companies(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id=company_id)
    if not company:
        raise HTTPException(detail="Company not found", status_code=404)
    return company


@router.get("/members")
async def get_members(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    members = await company_crud.get_members(company_id)
    return members


@router.post("/add")
async def add_company(company: company_schemas.AddCompany,
                      current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = basic_schemas.Company(**company.model_dump())
    company.owner_id = current_user.id
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(status_code=418)
    await user_crud.set_company(company_id=company.id, user_id=current_user.id)
    return company


@router.patch("/update")
async def update_company(company: company_schemas.RequestUpdateCompany,
                         current_user: user_schemas.User = Depends(Auth.get_current_user)):
    role = await Auth.get_role(user_id=current_user.id, company_id=company.id)
    if role < 2:
        raise HTTPException(detail="Only owner and admins can do it", status_code=403)
    company = company_schemas.UpdateCompany(**company.model_dump())
    company.owner_id = (await company_crud.get_company(company_id=company.id)).owner_id
    company = await company_crud.update(company=company)
    if not company:
        raise HTTPException(detail="Company not found", status_code=404)
    return company


@router.delete("/kick_user")
async def kick_user(company_id: int, user_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id)
    if company is None:
        HTTPException(detail="Company not found", status_code=404)

    current_user_role = await Auth.get_role(user_id=current_user.id, company_id=company_id)
    kicked_user_role = await Auth.get_role(user_id=user_id, company_id=company_id)
    if kicked_user_role < 1:
        raise HTTPException(detail="This user are not member of this company", status_code=403)
    if current_user_role < 2:
        raise HTTPException(detail="Only owner and admins can do it", status_code=403)
    if current_user_role < kicked_user_role:
        raise HTTPException(detail="Kicked user have too high role", status_code=403)
    if kicked_user_role > 1:
        admin = await admin_crud.get_by_user_id(user_id=user_id)
        admin_crud.delete(admin_id=admin.id)
    return await user_crud.set_company(None, user_id)


@router.delete("/delete_company")
async def delete_company(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id)
    if not company:
        HTTPException(detail="Company not found", status_code=404)
    role = await Auth.get_role(user_id=current_user.id, company_id=company.id)
    if role != 3:
        raise HTTPException(detail="Only owner can do it", status_code=403)
    company = await company_crud.delete(company_id=company_id)
    return company
