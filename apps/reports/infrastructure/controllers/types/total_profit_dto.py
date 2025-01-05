from pydantic import BaseModel

class TotalProfitsDto(BaseModel):
    profits: float