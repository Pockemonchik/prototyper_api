from typing import Any, Dict, List

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache

from src.api.schemas import APIErrorMessage
from src.core.logger import logger
from src.services.lessons_service import LessonsService

router = APIRouter()


# Read


@router.get(
    "/lessons",
    response_model=Dict[str, List[dict[str, Any]]],
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
    tags=["search"],
)
@cache(expire=5)
async def lessons_list(
    query: str = Query(
        None,
        examples=[
            "",
        ],
        description="Список уроков",
    ),
) -> JSONResponse:
    """Получение списка уроков"""

    logger.debug(f"lessons_list query:{query}")
    service = LessonsService()
    result = await service.get_lessons_list(query=query)

    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
