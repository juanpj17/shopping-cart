from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from apps.products.domain.product import Product
from apps.reports.application.queries.type.get_product_by_id_query import GetProductByIDQuery
from apps.reports.domain.total_profit import TotalProfit
from apps.reports.domain.total_profit_by_product import TotalProfitProduct
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetProductProfitsById(Service[str, TotalProfitProduct]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self, data: str):
        report = self.report_repository.get_product_total_profit_by_id(data)
        if not report: Result[str,TotalProfitProduct].make_failure(error = ProductNotFoundError())

        return Result[TotalProfitProduct].make_success(value = TotalProfitProduct(summary = report))
