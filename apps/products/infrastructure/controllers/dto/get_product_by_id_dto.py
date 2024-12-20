from pydantic import BaseModel

class GetProductByIdDto(BaseModel):
    id: str