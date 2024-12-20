from pydantic import BaseModel

class GetInventoryByProductResponse(BaseModel):
    product_id: str
    quantity: int