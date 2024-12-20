from abc import ABC, abstractmethod
from ..inventory import Inventory

class InventoryRepository(ABC):
    @abstractmethod
    def save_inventory(self, inventory: Inventory):
        pass

    @abstractmethod
    def get_inventory_by_product(self, product_id: str):
        pass

    @abstractmethod
    def get_all(self):
        pass
