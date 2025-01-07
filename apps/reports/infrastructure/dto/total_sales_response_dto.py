from dataclasses import dataclass

from apps.reports.domain.product_sales_report import ProductSalesReport

@dataclass
class SalesReportDTO:
    total_sales: int
    total_amount: float
    summary_by_product: list[ProductSalesReport]