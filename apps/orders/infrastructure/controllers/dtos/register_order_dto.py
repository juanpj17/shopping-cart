from pydantic import BaseModel

class RegisterOrderDto(BaseModel):
    cart_id: str
    user_id: str