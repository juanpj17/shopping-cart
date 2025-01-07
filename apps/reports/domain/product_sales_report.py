from dataclasses import dataclass


@dataclass
class ProductSalesReport:
    name: str
    quantity: int
    amount: float