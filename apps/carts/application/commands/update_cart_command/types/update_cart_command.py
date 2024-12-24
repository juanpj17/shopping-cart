from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    product_id: str
    quantity: int

class UpdateCartCommand(BaseModel):
    cart_id: str
    order_id: str
    products: List[Item]




