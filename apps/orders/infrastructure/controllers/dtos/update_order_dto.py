from pydantic import BaseModel

class UpdateOrderDto(BaseModel):
    order_id: str
    user_id: str
    status: str