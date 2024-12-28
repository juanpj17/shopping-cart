from pydantic import BaseModel, EmailStr

class UpdateUserDto(BaseModel):
    username: str
    email: EmailStr
    password: str
