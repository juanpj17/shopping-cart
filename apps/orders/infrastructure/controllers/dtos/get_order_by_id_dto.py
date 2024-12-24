from pydantic import BaseModel

class GetOrderByIdDto(BaseModel):
    order_id: str
