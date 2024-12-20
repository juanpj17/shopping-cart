from typing import List
from ....domain import User, UserRepository
from core.application.services.application_service import Service
from core.application.results.result import Result
from ...exceptions.no_users_found import NoUserFoundError

class GetAllUsersService(Service[None, List[User]]):

    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__()
        self.user_repository = user_repository

    def execute(self):
        users = self.user_repository.get_all_users()
        if (len(users) == 0):
            return Result[List[User]].make_failure(error=NoUserFoundError())
        
        return Result[List[User]].make_success(value=users)