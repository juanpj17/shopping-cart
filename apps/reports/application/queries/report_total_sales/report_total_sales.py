from apps.orders.application.exceptions.order_not_found import OrderNotFoundError
from apps.orders.domain.order import Order
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetTotalSales(Service[None, int]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self):
        report = self.report_repository.get_total_sales()
        if not report: Result[int].make_failure(error = OrderNotFoundError())

        return Result[int].make_success(value = report)