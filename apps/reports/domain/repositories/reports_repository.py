from abc import ABC, abstractmethod

class ReportsRepository(ABC):

    @abstractmethod
    def get_total_sales(self):
        pass

    @abstractmethod
    def get_total_profit(self):
        pass

    @abstractmethod
    def get_product_profit_by_id(self, id):
        pass

    @abstractmethod
    def get_product_sales_by_id(self, id):
        pass

    @abstractmethod
    def get_top_products(self):
        pass

    @abstractmethod
    def get_top_users(self):
        pass
