from pydantic import BaseModel

class RemoveProductFromCartCommand(BaseModel):
    user_id: str
    product_id: str