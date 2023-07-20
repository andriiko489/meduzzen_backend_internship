from fastapi import APIRouter

from services.logger import logger

router = APIRouter()


@router.get("/")
def health_check():
    logger.info("Someone check health")
    return {"status_code": 200,
            "detail": "ok",
            "result": "working"
            }
