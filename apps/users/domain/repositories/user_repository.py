from abc import ABC, abstractmethod 
from ..user import User

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self):
        pass

    @abstractmethod
    def get_user_by_username(self):
        pass
    
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def save_user(self, user: User):
        pass
