from .....domain.user import RoleEnum

class RegisterUserCommand():
    username: str
    email: str
    password: str
    role: RoleEnum
