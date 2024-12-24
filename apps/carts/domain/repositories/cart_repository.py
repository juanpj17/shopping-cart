from abc import ABC, abstractmethod
from ..cart import Cart

class CartRepository(ABC):

    @abstractmethod
    def save_cart(self, cart: Cart):
        pass

    @abstractmethod
    def get_cart_by_id(self):
        pass

    @abstractmethod
    def get_products_in_cart(self):
        pass

    @abstractmethod
    def get_cart_by_user(self):
        pass

    @abstractmethod
    def remove_product(self):
        pass

    @abstractmethod
    def archive_cart(self):
        pass

