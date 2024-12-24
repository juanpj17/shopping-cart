from pydantic import BaseModel
from typing import List, Optional

class GetCurrentUserCartResponse(BaseModel):
    cart_id: str
    order_id: Optional[str]
    product_id: str
    quantity: int
    price: float