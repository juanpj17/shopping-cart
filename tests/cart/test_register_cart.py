import pytest
from unittest.mock import MagicMock, patch,ANY
from core.application.results.result import Result
from apps.carts.application.commands.register_cart_command.register_cart import RegisterCartService
from apps.carts.application.commands.register_cart_command.types.register_cart_command import RegisterCartCommand
from apps.carts.domain.cart import Cart
from core.infrastructure.providers.uuid_service import UUIDService

def test_register_cart_success():
    # Mock del repositorio para guardar el carrito
    mock_repo = MagicMock()
    
    # Mock del servicio UUID para generar un ID específico
    with patch.object(UUIDService, 'generate_id', return_value="generated-uuid"):
        # Crear instancia del servicio con el repositorio mockeado
        service = RegisterCartService(mock_repo)
# Crear el comando de registro
        command = RegisterCartCommand(user_id="user123")

        # Ejecutar el servicio
        result = service.execute(command)

        # Validar el resultado
        assert result.is_success  # El resultado debe ser un éxito
        assert result.value == "generated-uuid"  # El valor devuelto debe ser el UUID generado
        

