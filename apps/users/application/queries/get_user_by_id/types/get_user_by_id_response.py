from .....domain.user import RoleEnum
from pydantic import BaseModel

class GetUserByIdResponse(BaseModel):
    id: str
    username: str
    email: str
    role: RoleEnum