import asyncio

import uvicorn

from src.core.api import api
from src.core.logger import logger

app = api


async def main() -> None:
    """Точка входа в приложение"""
    logger.info("run app")
    uvicorn.run("src.core.api:api", reload=True)


if __name__ == "__main__":
    asyncio.run(main())


# run
# sudo poetry run python -m src.main
