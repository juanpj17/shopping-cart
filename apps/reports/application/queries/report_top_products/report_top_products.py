from typing import List, Tuple
from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from apps.reports.domain.top_products_report import TopProducts
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTopProducts(Service[None, TopProducts]): 
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        report = self.report_repository.get_top_products()
        if not report: Result[TopProducts].make_failure(error = ProductNotFoundError())

        return Result[TopProducts].make_success(value = TopProducts(top_products=report))