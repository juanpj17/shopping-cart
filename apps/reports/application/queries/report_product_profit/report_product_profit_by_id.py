from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from apps.products.domain.product import Product
from apps.reports.application.queries.type.get_product_by_id_query import GetProductByIDQuery
from core.application.services.application_service import Service
from core.application.results.result import Result
from ....infrastructure.repositories.postgre_reports_repository import ReportsRepository

class GetProductProfitsById(Service[GetProductByIDQuery, float]):
    def __init__(self, report_repository: ReportsRepository):
        self.report_repository = report_repository
    
    def execute(self, data: GetProductByIDQuery):
        report = self.report_repository.get_product_sales_by_id(data.product_id)
        if not report: Result[str,float].make_failure(error = ProductNotFoundError())

        return Result[str,float].make_success(value = report)