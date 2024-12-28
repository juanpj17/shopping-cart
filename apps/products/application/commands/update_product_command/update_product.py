from core.application.services.application_service import Service
from .types.product_command import UpdateProductCommand
from ....domain.repositories.product_repository import ProductRepository
from ...exceptions.product_not_found import ProductNotFoundError
from core.application.results.result import Result
from ....domain.product import Product
from ....domain.services.calculate_product_price import CalculateProductPriceService

class UpdateProductService(Service[UpdateProductCommand, str]):
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self, id:str, data: UpdateProductCommand): 
        response = self.product_repository.get_product_by_id(id)

        if not response: Result[str].make_failure(error=ProductNotFoundError())

        product = Product(
            _id = data.id,
            code = response.code,
            name = response.name,
            price = response.price,
            cost = response.cost,
            margin = response.margin,
            status = response.status
        )

        
        if data.name: product.name = data.name
        if data.cost: product.cost = data.cost
        if data.margin: product.margin = data.margin
        if data.status: product.status = data.status
        if data.cost and data.status:
            service = CalculateProductPriceService()
            price = service.execute({"cost": data.cost, "margin": data.margin})
            product.price = price


        self.product_repository.save_product(product)
        return Result[str].make_success(value=id)