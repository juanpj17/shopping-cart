from core.application.services.application_service import Service
from .types.command import LoginCommand
from .....users.domain import UserRepository
from typing import Dict
from core.application.services.application_service import Service
from core.application.results.result import Result
from core.infrastructure.providers.crypto_service import CryptoService
from ....infrastructure.providers.jwt_services import JwtService
from .types import LoginCommand
from fastapi import HTTPException, status

class LoginService(Service[LoginCommand, str]):
        def __init__(self, user_repository: UserRepository) -> None:
            super().__init__()
            self.user_repository = user_repository
            self.cryptoService = CryptoService
            self.jwtService = JwtService
        
        def execute(self, data: LoginCommand) -> Result[Dict[str, str]]:
            user = self.user_repository.get_user_by_username(data.username)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
            if not self.cryptoService.check_password(data.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password."
                )
            return Result[Dict[str, str]].make_success({
                "access_token": self.jwtService.generateToken(user.entity_id, user.role),
                "token_type": "bearer"
            })