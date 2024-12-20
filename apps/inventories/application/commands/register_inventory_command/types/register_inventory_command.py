from pydantic import BaseModel

class RegisterInventoryCommand(BaseModel):
    product_id: str