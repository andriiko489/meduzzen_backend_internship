from fastapi import APIRouter, HTTPException, Depends

from crud.CompanyCRUD import company_crud
from schemas import schemas
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
async def add_company(company: schemas.AddCompany, current_user: schemas.User = Depends(Auth.get_current_user)):
    company = schemas.Company(**eval(company.model_dump_json()))
    company.owner = current_user
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(status_code=418)
    return company
