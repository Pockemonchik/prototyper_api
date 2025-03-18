import asyncio

import uvicorn


from .core.logger import logger


async def main() -> None:
    """Точка входа в приложение"""
    logger.info("run app")
    uvicorn.run("src.main:app", reload=True)


if __name__ == "__main__":
    asyncio.run(main())


# run
# sudo poetry run python -m src.main
