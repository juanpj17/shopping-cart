from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    product_id: str
    quantity: int

class UpdateCartDto(BaseModel):
    cart_id: str
    products: List[Item]
