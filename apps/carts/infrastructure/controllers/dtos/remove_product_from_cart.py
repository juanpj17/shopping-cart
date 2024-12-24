from pydantic import BaseModel

class RemoveProductFromCartDto(BaseModel):
    user_id: str
    product_id: str
