from pydantic import BaseModel

class GetProductByIDQuery(BaseModel):
    product_id: str