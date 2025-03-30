from src.texts.models import TextModel
from src.texts.schemas import TextSchema
from src.database.base_repository import BaseSqlAlchemyRepository


class TextRepository(BaseSqlAlchemyRepository):
    """Репозиторий текстами"""

    model: type[TextModel] = TextModel
    entity_schema = TextSchema
    create_schema = TextSchema
    update_schema = TextSchema
