from pydantic import BaseModel

class GetProductByIdResponse(BaseModel):
    id : str
    code: str
    name: str
    price: float 
    cost: float
    margin: float