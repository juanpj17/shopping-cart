from pydantic import BaseModel

class RegisterOrderCommand(BaseModel):
    user_id: str
    cart_id: str
    