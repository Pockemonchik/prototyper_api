from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache


from src.core.schemas import APIErrorMessage

router = APIRouter(
    prefix="/texts",
    tags=["texts"],
)


@router.get(
    "/",
    response_model=str,
    responses={
        400: {"model": APIErrorMessage},
        500: {"model": APIErrorMessage},
    },
)
@cache(expire=1)
async def get_text() -> JSONResponse:
    """Получение текста"""

    response_data = {
        "id": 1,
        "text": """Lorem ipsum dolor sit amet, consectetur adipiscing elit""",
    }

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
