import pytest
from unittest.mock import MagicMock
from apps.users.application.commands.register_user_command.register_user import RegisterUserService
from apps.users.application.commands.register_user_command.types.command import RegisterUserCommand
from apps.users.domain.user import User,RoleEnum
from core.application.results.result import Result
from apps.users.application.exceptions.superuser_created import SuperUserAlreadyCreated
from core.infrastructure.providers.crypto_service import CryptoService
from core.infrastructure.providers.uuid_service import UUIDService

#Act
def test_register_user_service_success():
    # Crear un comando de registro válido
    command = RegisterUserCommand()
    command.username="newuser"
    command.email="newuser@example.com"
    command.password="password123"
    command.role=RoleEnum.CLIENT
    
# Simular el repositorio, generador de ID y servicio de cifrado
    mock_user_repository = MagicMock()
    mock_user_repository.find_admin_user.return_value = []

    mock_id_generator = MagicMock()
    mock_id_generator.generate_id.return_value = "generated-uuid"

    mock_crypto_service = MagicMock()
    mock_crypto_service.encrypt_password.return_value = "encrypted-password"

    # Instanciar el servicio
    service = RegisterUserService(user_repository=mock_user_repository)
    service.idGenerator = mock_id_generator
    service.cryptoService = mock_crypto_service
 # Ejecutar el servicio
    result = service.execute(command)

    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert result.value == "generated-uuid"

 # Verificar que el usuario se guardó correctamente
    mock_user_repository.save_user.assert_called_once() 
    saved_user = mock_user_repository.save_user.call_args[0][0]
    assert saved_user.username == "newuser"


def test_register_user_service_superuser_already_exists():
    # Crear un comando para registrar un superadmin
    command = RegisterUserCommand()
    command.username="adminuser"
    command.email="admin@example.com"
    command.password="securepass"
    command.role=RoleEnum.ADMIN
    

    # Simular un repositorio que ya tiene un superadmin
    mock_user_repository = MagicMock()
    mock_user_repository.find_admin_user.return_value = [
        User(_id="1", username="existingadmin", email="admin@example.com", password="hashedpass", role=RoleEnum.ADMIN),
    ]

    # Instanciar el servicio
    service = RegisterUserService(user_repository=mock_user_repository)

    # Ejecutar el servicio
    result = service.execute(command)

    # Verificar que el resultado es un fallo
    assert result.is_failure()
    assert isinstance(result.error, SuperUserAlreadyCreated)
    assert result.error.message == "Superuser can be created just once"


def test_register_user_service_generate_id_and_encrypt_password():
    command = RegisterUserCommand()
    command.username = "newuser"
    command.email = "newuser@example.com"
    command.password = "password123"
    command.role = RoleEnum.CLIENT

    # Simular el repositorio
    mock_user_repository = MagicMock()
    mock_user_repository.find_admin_user.return_value = []

    # Simular UUIDService y CryptoService
    mock_id_generator = MagicMock()
    mock_id_generator.generate_id.return_value = "generated-uuid"
    mock_crypto_service = MagicMock()
    mock_crypto_service.encrypt_password.return_value = "encrypted-password"

    # Instanciar el servicio
    service = RegisterUserService(user_repository=mock_user_repository)
    service.idGenerator = mock_id_generator  # Sobrescribir instancia
    service.cryptoService = mock_crypto_service  # Sobrescribir instancia
    # Ejecutar el servicio
    result = service.execute(command)

    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert result.value == "generated-uuid"

    # Verificar que el usuario se guardó correctamente
    mock_user_repository.save_user.assert_called_once()
    saved_user = mock_user_repository.save_user.call_args[0][0]

    assert saved_user.username == command.username
    assert saved_user.email == command.email
    assert saved_user.password == "encrypted-password"
    assert saved_user.role == command.role