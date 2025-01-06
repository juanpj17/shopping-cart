import pytest
from unittest.mock import MagicMock
from core.application.results.result import Result
from apps.users.application.commands.update_user_command.update_user import UpdateUserService
from apps.users.application.commands.update_user_command.types.command import UpdateUserCommand
from apps.users.domain.user import User
from apps.users.application.exceptions.user_not_found import UserNotFoundError


def test_update_user_service_success():
    # Crear comando de actualización válido
    command = UpdateUserCommand()
    command.username = "updateduser"
    command.email = "updateduser@example.com"
    command.password = "newpassword123"

    # Simular el repositorio de usuarios
    mock_user_repository = MagicMock()
    mock_user_repository.get_user_by_id.return_value = MagicMock(
        entity_id="user-id",
        username="olduser",
        email="olduser@example.com",
        password="oldpassword",
        role="Client"
    )
    mock_user_repository.save_user = MagicMock()

    # Simular CryptoService
    mock_crypto_service = MagicMock()
    mock_crypto_service.encrypt_password.return_value = "encrypted-password"

    # Instanciar el servicio
    service = UpdateUserService(user_repository=mock_user_repository)
    service.cryptoService = mock_crypto_service  # Sobrescribir el servicio de cifrado

    # Ejecutar el servicio
    result = service.execute("user-id", command)

    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert result.value == "user-id"

    # Verificar que el usuario se actualizó correctamente
    mock_user_repository.save_user.assert_called_once()
    updated_user = mock_user_repository.save_user.call_args[0][0]

    assert updated_user.username == command.username
    assert updated_user.email == command.email
    assert updated_user.password == "encrypted-password"


def test_update_user_service_user_not_found():
    # Simular el repositorio de usuarios sin resultados
    mock_user_repository = MagicMock()
    mock_user_repository.get_user_by_id.return_value = None

    # Instanciar el servicio
    service = UpdateUserService(user_repository=mock_user_repository)

    # Crear un comando vacío
    command = UpdateUserCommand()

    # Ejecutar el servicio
    result = service.execute("nonexistent-id", command)

    # Verificar que el resultado es un error
    assert result.is_failure()
    assert isinstance(result.unwrap(), UserNotFoundError)
    mock_user_repository.save_user.assert_not_called()


def test_update_user_service_partial_update():
    # Crear un comando que solo actualiza el correo electrónico
    command = UpdateUserCommand()
    command.email = "partialupdate@example.com"

    # Simular el repositorio de usuarios
    mock_user_repository = MagicMock()
    mock_user_repository.get_user_by_id.return_value = MagicMock(
        entity_id="user-id",
        username="olduser",
        email="olduser@example.com",
        password="oldpassword",
        role="Client"
    )
    mock_user_repository.save_user = MagicMock()

    # Simular CryptoService
    mock_crypto_service = MagicMock()

    # Instanciar el servicio
    service = UpdateUserService(user_repository=mock_user_repository)
    service.cryptoService = mock_crypto_service  # Sobrescribir el servicio de cifrado

    # Ejecutar el servicio
    result = service.execute("user-id", command)

    # Verificar que el resultado es exitoso
    assert result.is_success()

    # Verificar que solo se actualizó el correo electrónico
    updated_user = mock_user_repository.save_user.call_args[0][0]
    assert updated_user.email == command.email
    assert updated_user.username == "olduser"
    assert updated_user.password == "oldpassword"
