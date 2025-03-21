class UserError(Exception):
    @classmethod
    def invalid_id(cls) -> "UserError":
        return cls("Invalid node id passed")


class AuthError(Exception):
    pass
