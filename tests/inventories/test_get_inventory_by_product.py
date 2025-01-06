from unittest.mock import MagicMock
from apps.inventories.application.queries.get_inventory_by_product.get_inventory_by_product import GetInventoryByProductService
from apps.inventories.application.queries.get_inventory_by_product.types.get_inventory_by_product_dto  import GetInventoryByProductDto
from apps.inventories.application.queries.get_inventory_by_product.types.get_inventory_by_product_response import GetInventoryByProductResponse
from apps.inventories.domain.inventory import Inventory
from core.application.results.result import Result
from apps.inventories.application.exceptions.inventory_not_found import InventoryNotFoundError

def test_get_inventory_by_product_success():
    # Mock del repositorio
    mock_repo = MagicMock()
    mock_repo.get_inventory_by_product.return_value = Inventory(
        _id="inventory123", product_id="product123", quantity=50
    )
# Crear una instancia del servicio con el repositorio mockeado
    service = GetInventoryByProductService(mock_repo)

    # Crear el DTO de entrada
    dto = GetInventoryByProductDto()
    dto.product_id="product123"
     # Ejecutar el método
    result = service.execute(dto)

# Verificar que el resultado es exitoso
    assert result.is_success
    assert isinstance(result.value, GetInventoryByProductResponse)
    assert result.value.product_id == "product123"
    assert result.value.quantity == 50

    # Verificar que el repositorio fue llamado correctamente
    mock_repo.get_inventory_by_product.assert_called_once_with("product123")

def test_get_inventory_by_product_not_found():
    # Mock del repositorio para devolver None
    mock_repo = MagicMock()
    mock_repo.get_inventory_by_product.return_value = None

    # Crear una instancia del servicio con el repositorio mockeado
    service = GetInventoryByProductService(mock_repo)

    # Crear el DTO de entrada
    dto = GetInventoryByProductDto()
    dto.product_id="nonexistent"

    # Ejecutar el método
    result = service.execute(dto)
    assert isinstance(result.error, InventoryNotFoundError)
    assert result.error.message == "Inventory not found"

#porque una lista de error