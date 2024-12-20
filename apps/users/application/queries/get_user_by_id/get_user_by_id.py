from core.application.services.application_service import Service
from .types.get_user_by_id_query import GetUserByIdQuery
from .types.get_user_by_id_response import GetUserByIdResponse
from ....domain.repositories.user_repository import UserRepository
from ...exceptions.user_not_found import UserNotFoundError
from core.application.results.result import Result

class GetUserByIdService(Service[GetUserByIdQuery, GetUserByIdResponse]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, data: GetUserByIdQuery ):
        response = self.user_repository.get_user_by_id(data.id)
        if not response: return Result[GetUserByIdResponse].make_failure(error=UserNotFoundError())

        user = GetUserByIdResponse(
            id = response.entity_id,
            username = response.username,
            email = response.email,
            role = response.role
        )
        return Result[GetUserByIdResponse].make_success(value=user)
