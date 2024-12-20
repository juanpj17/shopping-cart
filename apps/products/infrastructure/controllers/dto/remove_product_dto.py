from pydantic import BaseModel

class RemoveProductDto(BaseModel):
    id: str
