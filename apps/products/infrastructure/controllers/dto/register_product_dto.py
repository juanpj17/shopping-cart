from pydantic import BaseModel

class RegisterProductDto(BaseModel):
    name: str
    cost: float
    margin: float
    status: str