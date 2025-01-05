from pydantic import BaseModel

class ProductProfitByIdDto(BaseModel):
    id: str
    profit: int