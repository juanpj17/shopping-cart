from pydantic import BaseModel

class GetCurrentUserCartDto(BaseModel):
    user_id: str