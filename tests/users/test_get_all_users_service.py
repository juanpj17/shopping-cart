import pytest
from unittest.mock import MagicMock
from apps.users.application.queries.get_all_users_query.get_all_users import GetAllUsersService
from apps.users.domain.user import User
from core.application.results.result import Result
from apps.users.application.exceptions.no_users_found import NoUserFoundError


#Arrange
def test_get_all_users_service_success():
    # Crear una lista simulada de usuarios
    mock_users = [
        User(_id="1", username="user1", email="user1@example.com", password="pass1", role="Admin"),
        User(_id="2", username="user2", email="user2@example.com", password="pass2", role="Client"),
    ]
 # Crear un mock del repositorio
    mock_user_repository = MagicMock()
    mock_user_repository.get_all_users.return_value = mock_users

    # Instanciar el servicio con el repositorio simulado
    service = GetAllUsersService(user_repository=mock_user_repository)
#Act
 # Ejecutar el servicio
    result = service.execute()
#Arrange
    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert len(result.value) == 2
    assert result.value[0].username == "user1"
    assert result.value[1].username == "user2"

def test_get_all_users_service_no_users_found():
    # Crear un mock del repositorio que retorna una lista vacía
    mock_user_repository = MagicMock()
    mock_user_repository.get_all_users.return_value = []

    # Instanciar el servicio con el repositorio simulado
    service = GetAllUsersService(user_repository=mock_user_repository)

    # Ejecutar el servicio
    result = service.execute()

    # Verificar que el resultado es un fallo
    assert result.is_failure()
    assert isinstance(result.error, NoUserFoundError)
    assert result.error.message == 'No users found'  
