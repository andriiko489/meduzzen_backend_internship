from fastapi import APIRouter, Depends

from schemas import user_schemas
from services.auth import Auth
from utils.logger import logger

router = APIRouter()


@router.get("/")
def health_check(current_user: user_schemas.User = Depends(Auth.get_current_user)):
    logger.info("Someone check health")
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }
