from unittest.mock import MagicMock
from apps.products.application.commands.remove_product_command.remove_product import RemoveProductService
from apps.products.application.commands.remove_product_command.types.product_command import RemoveProductCommand
from apps.products.domain.product import Product
from core.application.results.result import Result
from apps.products.application.exceptions.product_not_found import ProductNotFoundError

def test_remove_product_service_success():
    # Crear un producto simulado
    existing_product = Product(
        _id="123",
        code="P001",
        name="Test Product",
        description="Product test",
        price=100.0,
        cost=60.0,
        margin=40.0,
        status="active"
    )

    # Simular el repositorio
    mock_product_repository = MagicMock()
    mock_product_repository.get_product_by_id.return_value = existing_product
    mock_product_repository.remove_product = MagicMock()

    # Crear instancia del servicio
    remove_product_service = RemoveProductService(product_repository=mock_product_repository)

    # Crear comando para eliminar el producto
    remove_command = RemoveProductCommand()
    remove_command.id="123"

    # Ejecutar el servicio
    result = remove_product_service.execute(remove_command)

    # Verificaciones
    assert result.is_success()
    assert result.value == "Product deleted correctly"

    # Verificar que el producto fue consultado y eliminado
    mock_product_repository.get_product_by_id.assert_called_once_with(remove_command)
    mock_product_repository.remove_product.assert_called_once_with(remove_command)

def test_remove_product_service_product_not_found():
    # Simular el repositorio
    mock_product_repository = MagicMock()
    mock_product_repository.get_product_by_id.return_value = None  # Producto no encontrado

    # Crear instancia del servicio
    remove_product_service = RemoveProductService(product_repository=mock_product_repository)

    # Crear comando para eliminar el producto
    remove_command = RemoveProductCommand()
    remove_command="123"

    # Ejecutar el servicio
    result = remove_product_service.execute(remove_command)

    # Verificaciones
    assert result.is_failure()
    assert isinstance(result.error, ProductNotFoundError)

    # Verificar que remove_product no fue llamado
    mock_product_repository.remove_product.assert_not_called()