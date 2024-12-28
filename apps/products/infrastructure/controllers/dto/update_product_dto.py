from pydantic import BaseModel

class UpdateProductDto(BaseModel):
    name: str
    cost: float
    margin: float
    status: str