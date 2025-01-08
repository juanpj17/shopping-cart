from dataclasses import dataclass

from apps.reports.domain.product_sales_report import ProductSalesReport

@dataclass
class ProductSalesReportDTO:
    summary: ProductSalesReport