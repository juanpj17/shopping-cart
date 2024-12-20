from core.domain.entity.domain_entity import DomainEntity
from enum import Enum
 
class RoleEnum(str, Enum):
    ADMIN = "Superadmin"
    MANAGER = "Manager"
    CLIENT = "Client"

class User(DomainEntity[str]):
    def __init__(self, _id: str, username: str, email: str, password: str, role: RoleEnum) -> None:
        super().__init__(_id)
        self.username = username
        self.email = email
        self.password = password
        self.role = role
     
    def update_username(self, username: str):
        self.username = username

    def update_email(self, email: str):
        self.email = email

    def update_password(self, password: str):
        self.password = password
