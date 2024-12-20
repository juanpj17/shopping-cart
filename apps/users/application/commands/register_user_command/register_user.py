from core.application.services.application_service import Service
from core.infrastructure.providers.crypto_service import CryptoService
from core.infrastructure.providers.uuid_service import UUIDService
from apps.users.application.commands.register_user_command.types.command import RegisterUserCommand
from ....domain.user import User
from ....domain import UserRepository
from core.application.results.result import Result


class RegisterUserService(Service[RegisterUserCommand, str]):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.idGenerator = UUIDService
        self.cryptoService = CryptoService

    def execute(self, data: RegisterUserCommand):
        id = self.idGenerator.generate_id()
        password = self.cryptoService.encrypt_password(data.password)
        user = User(id, data.username, data.email, password, data.role)
        self.user_repository.save_user(user)
        return Result[str].make_success(value=id)
