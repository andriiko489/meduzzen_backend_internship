from fastapi import APIRouter, HTTPException

from crud.CompanyCRUD import company_crud
from schemas import company
from utils.logger import logger

router = APIRouter(
    prefix="/company",
    tags=["company"])


@router.get("/all/")
async def get_company() -> list[company.Company]:
    logger.info("Someone want list of all users")
    return await company_crud.get_companies()


@router.get("/get")
async def get_companies(company_id: int):
    company = await company_crud.get_company(company_id=company_id)
    if not company:
        raise HTTPException(detail="User not found", status_code=404)
    return company


@router.post("/add")
async def sign_up_company(company: company.Company):
    company = await company_crud.add(company=company)
    if not company:
        raise HTTPException(detail="User with this email or username already exist", status_code=418)
    return company
