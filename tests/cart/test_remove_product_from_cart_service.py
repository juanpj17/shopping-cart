import pytest
from unittest.mock import Mock
from core.application.results.result import Result
from core.application.services.application_service import Service
from apps.carts.application.commands.remove_product_from_cart_command.types.remove_product_from_cart_command import RemoveProductFromCartCommand
from apps.carts.domain.repositories.cart_repository import CartRepository
from  apps.carts.application.commands.remove_product_from_cart_command.remove_product_from_cart import RemoveProductFromCartService

@pytest.fixture
def mock_cart_repository():
    return Mock(spec=CartRepository)

@pytest.fixture
def service(mock_cart_repository):
    return RemoveProductFromCartService(cart_repository=mock_cart_repository)

def test_remove_product_from_cart_success(service, mock_cart_repository):
    # Configurar datos simulados
    mock_cart_repository.get_cart_by_user.return_value = ("cart123", ["prod1", "prod2"])
    
    command = RemoveProductFromCartCommand(user_id="user123", product_id="prod1")
    mock_cart_repository.remove_product.return_value = None  # Método sin retorno

     # Ejecutar el método
    result = service.execute(command)
      # Verificaciones
    mock_cart_repository.get_cart_by_user.assert_called_once_with("user123")
    mock_cart_repository.remove_product.assert_called_once_with("prod1")
    assert result.is_success
    assert result.value == "Product deletedc"

def test_remove_product_from_cart_empty_cart(service, mock_cart_repository):
    # Configurar datos simulados
    mock_cart_repository.get_cart_by_user.return_value = ("cart123", [])
    
    command = RemoveProductFromCartCommand(user_id="user123", product_id="prod1")

    # Ejecutar el método
    result = service.execute(command)

    # Verificaciones
    mock_cart_repository.get_cart_by_user.assert_called_once_with("user123")
    mock_cart_repository.remove_product.assert_not_called()  # No debería intentar eliminar
    assert result.is_success
    assert result.value == {"cart_id": "cart123", "products": 0}

def test_remove_product_from_cart_repository_error(service, mock_cart_repository):
    # Simular un error al obtener el carrito
    mock_cart_repository.get_cart_by_user.side_effect = Exception("Repository error")
    
    command = RemoveProductFromCartCommand(user_id="user123", product_id="prod1")

    # Ejecutar el método y verificar que lanza una excepción
    with pytest.raises(Exception, match="Repository error"):
        service.execute(command)

    # Verificar que no se intentó eliminar ningún producto
    mock_cart_repository.remove_product.assert_not_called()