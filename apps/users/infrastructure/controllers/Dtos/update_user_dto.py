from pydantic import BaseModel, EmailStr

class UpdateUserDto(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
