from pydantic import BaseModel

class UpdateProductDto(BaseModel):
    id: str
    name: str
    cost: float
    margin: float
    status: str