from core.application.services.application_service import Service
from ....domain.inventory import Inventory
from typing import List
from ....domain.repositories.inventory_repository import InventoryRepository
from core.application.results.result import Result
from ...exceptions.inventories_not_found import InventoriesNotFoundError

class GetAllInventoriesService(Service[None, List[Inventory]]):
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def execute(self):
        products = self.inventory_repository.get_all()
        if(len(products) == 0): 
            return Result[List[Inventory]].make_failure(error=InventoriesNotFoundError())
        return Result[List[Inventory]].make_success(value=products)