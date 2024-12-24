from core.domain.entity.domain_entity import DomainEntity
from enum import Enum
 
class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(DomainEntity[str]):
    def __init__(self, _id: str, user_id: str, cart_id: str, status: StatusEnum, total: float):
        super().__init__(_id)
        self.user_id = user_id
        self.cart_id = cart_id
        self.status = status
        self.total = total
    
    def update_status(self, status: StatusEnum):
        self.status = status
    
    def update_total(self, total: float):
        self.total = total