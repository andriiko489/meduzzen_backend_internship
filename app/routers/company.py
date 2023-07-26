from fastapi import APIRouter, HTTPException, Depends

from crud.CompanyCRUD import company_crud
from schemas import schemas, companies, users
from services.auth import Auth
from utils.logger import logger

router = APIRouter(
    prefix="/company",
    tags=["company"])


@router.get("/all/")
async def get_company():
    logger.info("Someone want list of all companies")
    return await company_crud.get_companies()


@router.get("/get")
async def get_companies(company_id: int):
    company = await company_crud.get_company(company_id=company_id)
    if not company:
        raise HTTPException(detail="Company not found", status_code=404)
    return company


@router.post("/add")
async def add_company(company: companies.AddCompany, current_user: users.User = Depends(Auth.get_current_user)):
    company = companies.Company(**eval(company.model_dump_json()))
    company.owner = current_user
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(status_code=418)
    return company


@router.patch("/update")
async def update_company(company: companies.RequestUpdateCompany, current_user: users.User = Depends(Auth.get_current_user)):
    company = companies.UpdateCompany(**company.model_dump())
    company.owner_id = current_user.id
    await company.model_validate(company)
    company = await company_crud.update(company=company)
    if not company:
        raise HTTPException(detail="Company not found", status_code=404)
    return company
