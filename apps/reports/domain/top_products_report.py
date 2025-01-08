from dataclasses import dataclass
from apps.reports.domain.top_product import TopProduct


@dataclass
class TopProducts:
    top_products: list[TopProduct]