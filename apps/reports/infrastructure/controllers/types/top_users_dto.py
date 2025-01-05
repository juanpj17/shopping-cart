from pydantic import BaseModel

class TopUsersDto(BaseModel):
    id: str
    orders: int