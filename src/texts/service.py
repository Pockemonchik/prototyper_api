from backend.src.texts.repository import TextRepository


class TextService:
    """Сервис управления текстами"""

    def __init__(
        self,
        text_repo: TextRepository,
    ):
        self.text_repo = text_repo
