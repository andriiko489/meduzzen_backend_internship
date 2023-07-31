from fastapi import APIRouter, HTTPException, Depends

from crud.CompanyCRUD import company_crud
from schemas import company_schemas, user_schemas
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
    company = company_schemas.Company(**company.model_dump())
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(status_code=418)
    return company


@router.patch("/update")
async def update_company(company: company_schemas.RequestUpdateCompany,
                         current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = company_schemas.UpdateCompany(**company.model_dump())
    await company.model_validate(company)
    company = await company_crud.update(company=company)
    if not company:
        raise HTTPException(detail="Company not found", status_code=404)
    return company


@router.delete("/delete")
async def delete_user(company_id: int, current_user: user_schemas.User = Depends(Auth.get_current_user)):
    company = await company_crud.get_company(company_id)
    if company is None:
        HTTPException(detail="Company not found", status_code=404)
    if company.owner_id != current_user.id:
        HTTPException(detail="Only owner can delete this company", status_code=403)
    company = await company_crud.delete(company_id=company_id)
    return company
