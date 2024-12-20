from core.application.services.application_service import Service
from .types.update_inventory_command import UpdateInventoryCommand
from ....domain.repositories.inventory_repository import InventoryRepository
from ....domain.inventory import Inventory
from ...exceptions.inventory_not_found import InventoryNotFoundError
from core.application.results.result import Result

class UpdateInventoryService(Service[UpdateInventoryCommand, str]):
    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def execute(self, data: UpdateInventoryCommand):
        response = self.inventory_repository.get_inventory_by_product(data.product_id)
        if not response:
            return Result[str].make_failure(error=InventoryNotFoundError())

        inventory = Inventory(_id = response.entity_id, product_id = data.product_id, quantity = response.quantity)
        if data.quantity: inventory.quantity = data.quantity
        self.inventory_repository.save_inventory(inventory)
        return Result[str].make_success(value=data.product_id)
        