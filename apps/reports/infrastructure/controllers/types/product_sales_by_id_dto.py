from pydantic import BaseModel

class ProductSalesByIdDto(BaseModel):
    id: str
    sales: int