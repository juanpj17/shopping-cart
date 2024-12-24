from pydantic import BaseModel

class GetOrderByIdQuery(BaseModel):
    order_id: str