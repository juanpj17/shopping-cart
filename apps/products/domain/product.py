from core.domain.entity.domain_entity import DomainEntity

class Product(DomainEntity[str]):
    def __init__(self, _id: str, code: str, name: str, price: float, cost: float, margin: float, status: str):
        super().__init__(_id)
        self.code = code
        self.name = name
        self.price = price 
        self.cost = cost
        self.margin = margin
        self.status = status

    def update_name(self, name: str):
        self.name = name
    
    def update_price(self, price: float):
        self.price = price

    def update_cost(self, cost: float):
        self.cost = cost

    def update_margin(self, margin: float):
        self.margin = margin
    
    def update_status(self, status: str):
        self.status = status