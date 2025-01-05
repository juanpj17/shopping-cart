from pydantic import BaseModel

class TopProductsDto(BaseModel):
    id: str
    sales: int