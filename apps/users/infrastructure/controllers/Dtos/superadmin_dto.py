from pydantic import BaseModel, EmailStr
from ....domain.user import RoleEnum

class SuperAdminDto(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.ADMIN