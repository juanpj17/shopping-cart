from pydantic import BaseModel

class LoginDto(BaseModel):
    username: str
    password: str