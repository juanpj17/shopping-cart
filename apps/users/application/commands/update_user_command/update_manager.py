from apps.users.application.exceptions.user_not_manager import UserNotManager
from core.application.services.application_service import Service
from core.infrastructure.providers.crypto_service import CryptoService
from apps.users.application.commands.update_user_command.types.command import UpdateUserCommand
from ....domain.user import User
from ....domain import UserRepository
from core.application.results.result import Result
from datetime import datetime
from ...exceptions.user_not_found import UserNotFoundError

class UpdateManagerService(Service[UpdateUserCommand, str]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.cryptoService = CryptoService

    def execute(self, id:str, data: UpdateUserCommand):
        response = self.user_repository.get_user_by_id(id)
        if not response: return Result[str].make_failure(error=UserNotFoundError())

        user = User(
            _id = response.entity_id, 
            username = response.username,
            email = response.email,
            password = response.password,
            role = response.role
        )

        if user is not None and user.role == 'Manager':
            if data.username: user.update_username(data.username)
            if data.email: user.update_email(data.email)
            if data.password: 
                password = self.cryptoService.encrypt_password(data.password)
                user.update_password(password)
            self.user_repository.save_user(user)
            return Result[str].make_success(value=id)
        return Result[str].make_failure(error=UserNotManager())