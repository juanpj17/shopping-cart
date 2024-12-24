from pydantic import BaseModel
from .....domain.order import StatusEnum

class UpdateOrderCommand(BaseModel):
    order_id: str
    user_id: str
    status: str