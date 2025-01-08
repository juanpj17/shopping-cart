import pytest
from unittest.mock import MagicMock
from core.application.results.result import Result
from apps.products.application.commands.update_product_command.update_product import UpdateProductService
from apps.products.application.commands.update_product_command.types.product_command import UpdateProductCommand
from apps.products.domain.product import Product
from apps.products.application.exceptions.product_not_found import ProductNotFoundError


def test_update_product_service_product_not_found():
#Arrange
    # Crear un repositorio simulado (mock)
    mock_product_repository = MagicMock()
    mock_product_repository.get_product_by_id.return_value = None
 # Crear instancia del servicio
    update_product_service = UpdateProductService(product_repository=mock_product_repository)
    update_command = UpdateProductCommand()
    update_command.id="999"
    update_command.name="Nonexistent Product"
    update_command.cost=50.0
    update_command.margin=10.0
    update_command.status="active"
#Act
      # Ejecutar el servicio y verificar el resultado
    result = update_product_service.execute("999", update_command)
#Assert
    assert result.is_failure()
    assert isinstance(result.error, ProductNotFoundError)
    mock_product_repository.save_product.assert_not_called()
    

def test_update_product_service_success():
#Arrange
    # Simular un producto existente
    existing_product = Product(
        _id="123",
        code="P001",
        name="Old Product Name",
        description="Test Product",
        price=100.0,
        cost=60.0,
        margin=40.0,
        status="active"
    )
# Crear un repositorio simulado
    mock_product_repository = MagicMock()
    mock_product_repository.get_product_by_id.return_value = existing_product
    mock_product_repository.save_product = MagicMock()
    # Crear instancia del servicio
    update_product_service = UpdateProductService(product_repository=mock_product_repository)
    update_command = UpdateProductCommand()
    update_command.id="123"
    update_command.name="Updated Product Name"
    update_command.cost=80.0
    update_command.margin=25.0
    update_command.status="inactive"

    # Ejecutar el servicio
    result = update_product_service.execute("123", update_command)
# Verificaciones
    assert result.is_success()
    assert result.value == "123"

# Verificar que el producto fue actualizado correctamente
    updated_product = mock_product_repository.save_product.call_args[0][0]
    assert updated_product.name == "Updated Product Name"
    assert updated_product.cost == 80.0
    assert updated_product.margin == 25.0
    assert updated_product.price == 106.67  # 80 / (1 - 0.25)
    assert updated_product.status == "inactive"
    # Verificar que el método save_product fue llamado una vez
    mock_product_repository.save_product.assert_called_once()