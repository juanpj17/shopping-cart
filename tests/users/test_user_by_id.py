import pytest
from unittest.mock import MagicMock
from core.application.services.application_service import Service
from core.application.results.result import Result
from  apps.users.application.queries.get_user_by_id.get_user_by_id import GetUserByIdService
from apps.users.application.queries.get_user_by_id.types.get_user_by_id_query import GetUserByIdQuery
from apps.users.application.queries.get_user_by_id.types.get_user_by_id_response import GetUserByIdResponse
from apps.users.application.exceptions.user_not_found import UserNotFoundError
from apps.users.domain.user import RoleEnum

# Prueba exitosa de GetUserByIdService

# Arrange
def test_get_user_by_id_service_success():
    # Crear el query de entrada
    query = GetUserByIdQuery()
    query.id = "123"
  # Crear una respuesta simulada del repositorio
    mock_user = MagicMock()
    mock_user.entity_id = "123"
    mock_user.username = "john_doe"
    mock_user.email = "john.doe@example.com"
    mock_user.role = RoleEnum.ADMIN

 # Crear un mock del repositorio
    mock_user_repository = MagicMock()
    mock_user_repository.get_user_by_id.return_value = mock_user
 # Instanciar el servicio con el repositorio simulado
    service = GetUserByIdService(user_repository=mock_user_repository)

#Act
  # Ejecutar el servicio
    result = service.execute(query)
#Assert
 # Verificar que el resultado es exitoso
    assert result.is_success()
    assert result.value.id == "123"
    assert result.value.username == "john_doe"
    assert result.value.email == "john.doe@example.com"
    assert result.value.role == RoleEnum.ADMIN

# Prueba fallida de GetUserByIdService
#Arrange
def test_get_user_by_id_service_user_not_found():
    # Crear el query de entrada
    query = GetUserByIdQuery()
    query.id = "123"

    # Crear un mock del repositorio que retorna None
    mock_user_repository = MagicMock()
    mock_user_repository.get_user_by_id.return_value = None

    # Instanciar el servicio con el repositorio simulado
    service = GetUserByIdService(user_repository=mock_user_repository)
#Act
    # Ejecutar el servicio
    result = service.execute(query)
#Assert
    # Verificar que el resultado es un fallo
    assert result.is_failure()
    assert isinstance(result.error, UserNotFoundError)
    assert result.error.message == "User not found"