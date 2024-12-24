from abc import ABC, abstractmethod
from ..order import Order

class OrderRepository(ABC):

    @abstractmethod
    def save_order(self, order: Order):
        pass

    @abstractmethod
    def get_order_by_id(self):
        pass

    @abstractmethod
    def get_all_orders(self):
        pass