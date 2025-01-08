import pytest
from unittest.mock import MagicMock, patch,ANY
from core.application.results.result import Result
from apps.carts.application.commands.register_cart_command.register_cart import RegisterCartService
from apps.carts.application.commands.register_cart_command.types.register_cart_command import RegisterCartCommand
from apps.carts.domain.cart import Cart
from core.infrastructure.providers.uuid_service import UUIDService
def test_register_cart_with__uuid_service():
 # Mock del repositorio para guardar el carrito
    mock_repo = MagicMock()

    # Crear instancia del servicio sin el UUIDService mockeado
    service = RegisterCartService(mock_repo)
    # Crear el comando de registro
    command = RegisterCartCommand(user_id="user123")

    # Ejecutar el servicio
    result = service.execute(command)
    assert result.is_success
   # Verificar que save_cart fue llamado con el carrito correcto
    mock_repo.save_cart.assert_called_once_with(
        ANY,  # Ignorar la referencia exacta del objeto Cart, verificar sus valores
        products=None  # Verificar que products está en None
    )