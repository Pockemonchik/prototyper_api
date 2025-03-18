from dataclasses import dataclass
from src.core.logger import logger


@dataclass
class LessonsService:
    """Сервис управления уроками"""

    async def get_lessons_list(self, query: str) -> str:
        logger.debug(f"get_lessons_list: {query}")
        return ""
