from pydantic import BaseModel

class TotalSalesDto(BaseModel):
    sales: int