from src.database.base_repository import BaseSqlAlchemyRepository
from src.users.models import UserModel


from src.users.schemas import CreateUserSchema, UserSchema, UpdateUserSchema


class UsersRepository(BaseSqlAlchemyRepository):
    model = UserModel
    entity_schema = UserSchema
    create_schema = CreateUserSchema
    update_schema = UpdateUserSchema
