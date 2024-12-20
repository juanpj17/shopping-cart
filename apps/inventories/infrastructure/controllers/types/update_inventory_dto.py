from pydantic import BaseModel

class UpdateInventoryDto(BaseModel):
    product_id: str
    quantity: int