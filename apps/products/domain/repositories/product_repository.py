from abc import ABC, abstractmethod 
from ..product import Product

class ProductRepository(ABC):

    @abstractmethod
    def save_product(self, product: Product):
        pass

    @abstractmethod
    def remove_product(self):
        pass

    @abstractmethod
    def get_product_by_id(self):
        pass

    @abstractmethod
    def get_all_products(self):
        pass
