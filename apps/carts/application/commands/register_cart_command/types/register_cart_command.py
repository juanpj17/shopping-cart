from pydantic import BaseModel

class RegisterCartCommand(BaseModel):
    user_id: str

