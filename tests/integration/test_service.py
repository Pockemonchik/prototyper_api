import pytest

from src.services.lessons_service import LessonsService


@pytest.mark.asyncio
async def test_can_get_lessons():
    # given
    query = "Бабель Михаил Александрович"
    service = LessonsService()
    # when

    result = await service.get_lessons_list(query=query)
    # then
    assert result == "result"
