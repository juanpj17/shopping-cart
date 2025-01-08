from dataclasses import dataclass
from apps.reports.domain.total_profit import TotalProfit

@dataclass
class ProfitSalesReportDTO:
    total_income: float
    total_profit: float
    summary_by_product: list[TotalProfit]