from apps.orders.application.exceptions.order_not_found import OrderNotFoundError
from apps.orders.domain.order import Order
from apps.reports.infrastructure.dto.total_sales_response_dto import SalesReportDTO
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTotalSales(Service[None, SalesReportDTO]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        sales = self.report_repository.get_total_sales()
        total = self.report_repository.get_total_sales_amount()
        product_sales = self.report_repository.get_sales_by_products()
        if not sales: Result[SalesReportDTO].make_failure(error = OrderNotFoundError())
        if not total: Result[SalesReportDTO].make_failure(error = OrderNotFoundError())

        return Result[SalesReportDTO].make_success(value = SalesReportDTO(total_sales=sales, total_amount=total, summary_by_product=product_sales))