from dataclasses import dataclass
from apps.reports.domain.total_profit import TotalProfit

@dataclass
class TotalProfitProduct:
    summary: TotalProfit