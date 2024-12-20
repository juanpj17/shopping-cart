from pydantic import BaseModel

class GetUserByIdDto(BaseModel):
    id : str
