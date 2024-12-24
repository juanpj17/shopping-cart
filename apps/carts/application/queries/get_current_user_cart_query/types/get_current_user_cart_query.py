from pydantic import BaseModel

class GetCurrentUserCartQuery(BaseModel):
    user_id:str