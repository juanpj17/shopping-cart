from core.domain.entity.domain_entity import DomainEntity
from typing import List


class Cart(DomainEntity[str]):
    def __init__(self, _id: str, user_id: str, order_id: str | None, products: List[str] | None):
        super().__init__(_id)
        self.user_id = user_id
        self.order_id = order_id
        self.products = products
    
    def add_product(self, product_id: str):
        self.product_id.append(product_id)
    
    