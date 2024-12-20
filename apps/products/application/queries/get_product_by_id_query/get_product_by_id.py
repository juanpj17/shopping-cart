from ....domain.product import Product
from ....domain.repositories.product_repository import ProductRepository
from core.application.services.application_service import Service
from core.application.results.result import Result
from .types.product_query import GetProductByIdQuery
from ...exceptions.product_not_found import ProductNotFoundError
from .types.product_response import GetProductByIdResponse

class GetProductByIdService(Service[GetProductByIdQuery, GetProductByIdResponse]):

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, data: GetProductByIdQuery):
        response = self.product_repository.get_product_by_id(data.id)
        if not response: Result[GetProductByIdResponse].make_failure(error = ProductNotFoundError())
        product = GetProductByIdResponse(
            id = data.id,
            code = response.code,
            name = response.name,
            price = response.price,
            cost = response.cost,
            margin = response.margin,
            status = response.status
        )
        return Result[GetProductByIdResponse].make_success(value=product)