from pydantic import BaseModel

class UpdateInventoryCommand(BaseModel):
    product_id: str
    quantity: str