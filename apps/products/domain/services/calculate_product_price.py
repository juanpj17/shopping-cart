from core.domain.services.domain_service import DomainService
from typing import Optional

class CalculateProductPriceService(DomainService[dict, float]):

    def execute(self, data: Optional[dict] = None) -> float:
        
        cost = data.get("cost")
        margin = data.get("margin")

        if margin is None or not (0 <= margin):
            raise ValueError("Margin must be positive")
        if cost is None or cost < 0:
            raise ValueError("Cost must be positive.")

        precio = cost / (1 - margin/100)
        return round(precio, 2)