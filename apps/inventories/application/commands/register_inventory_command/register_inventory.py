from core.application.services.application_service import Service
from core.application.events.subscriber import Subscriber
from .types.register_inventory_command import RegisterInventoryCommand
from ....domain.repositories.inventory_repository import InventoryRepository
from core.infrastructure.providers.uuid_service import UUIDService
from ....domain.inventory import Inventory


class RegisterInventoryService(Service[RegisterInventoryCommand, None], Subscriber[RegisterInventoryCommand]):
    def __init__(self, inventory_repository: InventoryRepository):
        self.uuid_service = UUIDService
        self.inventory_repository = inventory_repository
 
    def update(self, data: RegisterInventoryCommand):
        self.execute(data)
        
    def execute(self, data: RegisterInventoryCommand):
        _id = self.uuid_service.generate_id()
        inventory = Inventory(_id, data.product_id, 0)
        self.inventory_repository.save_inventory(inventory)     