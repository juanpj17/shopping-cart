from core.application.services.application_service import Service
from ....domain.inventory import Inventory
from typing import List
from ....domain.repositories.inventory_repository import InventoryRepository
from core.application.results.result import Result
from ...exceptions.inventory_not_found import InventoryNotFoundError
from .types.get_inventory_by_product_dto import GetInventoryByProductDto
from .types.get_inventory_by_product_response import GetInventoryByProductResponse

class GetInventoryByProductService(Service[GetInventoryByProductDto, GetInventoryByProductResponse]):
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def execute(self, data: GetInventoryByProductDto):
        product = self.inventory_repository.get_inventory_by_product(data.product_id)
        if not product: 
            return Result[List[Inventory]].make_failure(error=InventoryNotFoundError())
        product = GetInventoryByProductResponse(product_id = data.product_id, quantity = product.quantity)
        return Result[List[GetInventoryByProductResponse]].make_success(value=product)