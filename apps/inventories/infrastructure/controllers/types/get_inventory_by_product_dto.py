from pydantic import BaseModel

class GetInventoryByProductDto(BaseModel):
    product_id: str