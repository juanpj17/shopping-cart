from pydantic import BaseModel

class RegisterProductDto(BaseModel):
    code: str
    name: str
    description: str
    cost: float
    margin: float
    status: str