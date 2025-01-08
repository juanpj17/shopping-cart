from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from apps.products.domain.product import Product
from apps.reports.infrastructure.dto.total_profit_response_dto import ProfitSalesReportDTO
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTotalProfits(Service[None, ProfitSalesReportDTO]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        report = self.report_repository.get_total_profit()
        products = self.report_repository.get_total_profit_by_products()
        if not report: Result[ProfitSalesReportDTO].make_failure(error = ProductNotFoundError())
        if not products: Result[ProfitSalesReportDTO].make_failure(error = ProductNotFoundError())

        return Result[ProfitSalesReportDTO].make_success(value = ProfitSalesReportDTO(
            total_income = report.total_income,
            total_profit = report.total_profit,
            summary_by_product = products
        ))