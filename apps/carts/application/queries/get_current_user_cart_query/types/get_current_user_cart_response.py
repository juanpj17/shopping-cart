from pydantic import BaseModel
from typing import List

class GetCurrentUserCartResponse(BaseModel):
    cart_id: str
    product_id: str
    quantity: int
    price: float