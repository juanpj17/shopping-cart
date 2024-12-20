from core.domain.entity.domain_entity import DomainEntity

class Inventory(DomainEntity[str]):

    def __init__(self, _id: str, product_id: str, quantity: int):
        super().__init__(_id)
        self.product_id = product_id
        self.quantity = quantity

    def update_product_quantity(self, quantity: int):
        self.quantity = quantity