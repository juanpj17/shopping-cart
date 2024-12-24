from pydantic import BaseModel

class RegisterCartDto(BaseModel):
    user_id: str