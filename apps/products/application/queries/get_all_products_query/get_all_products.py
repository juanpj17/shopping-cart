from typing import List
from ....domain.product import Product
from ....domain.repositories.product_repository import ProductRepository
from core.application.services.application_service import Service
from core.application.results.result import Result
from ...exceptions.products_not_found import ProductsNotFoundError

class GetAllProductsService(Service[None, List[Product]]):

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def execute(self):
        products = self.product_repository.get_all_products()
        if (len(products) == 0):
            return Result[List[Product]].make_failure(error=ProductsNotFoundError())
        
        return Result[List[products]].make_success(value=products)