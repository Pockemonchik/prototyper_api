from src.core.errors import ResourceNotFoundError


class UserError(Exception):
    @classmethod
    def invalid_id(cls) -> "UserError":
        return cls("Invalid node id passed")


class UserNotfoundError(ResourceNotFoundError):
    pass


class AuthError(Exception):
    pass
