from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from apps.products.domain.product import Product
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTotalProfits(Service[None, float]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        report = self.report_repository.get_total_profit()
        if not report: Result[float].make_failure(error = ProductNotFoundError())

        return Result[float].make_success(value = report)