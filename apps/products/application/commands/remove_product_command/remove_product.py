from .types.product_command import RemoveProductCommand
from ...exceptions.product_not_found import ProductNotFoundError
from core.application.services.application_service import Service
from ....domain.repositories.product_repository import ProductRepository
from core.application.results.result import Result

class RemoveProductService(Service[RemoveProductCommand, str]):
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, data: RemoveProductCommand):
        product = self.product_repository.get_product_by_id(data)
        if not product: Result[str].make_failure(error=ProductNotFoundError())
        self.product_repository.remove_product(data)
        return Result[str].make_success(value="Product deleted correctly") 
        