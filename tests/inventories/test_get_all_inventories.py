import pytest
from unittest.mock import MagicMock
from core.application.results.result import Result
from apps.inventories.domain.inventory import Inventory
from apps.inventories.application.exceptions.inventories_not_found import InventoriesNotFoundError
from  apps.inventories.application.queries.get_all_inventories_query.get_all_inventories import GetAllInventoriesService

def test_get_all_inventories_no_products():
# Mock del repositorio para devolver una lista vacía
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = []

# Crear instancia del servicio con el repositorio mockeado
    service = GetAllInventoriesService(mock_repo)
# Ejecutar el servicio
    result = service.execute()
# Validar los resultados  
    assert isinstance(result.error, InventoriesNotFoundError)  # Validar que el error sea el esperado
    assert result.error.message == "Inventories not found"  # Mensaje personalizado

def test_get_all_inventories_with_products():
    # Mock del repositorio para devolver una lista de inventarios
    mock_repo = MagicMock()
    mock_repo.get_all.return_value = [
        Inventory(_id="1", product_id="prod1", quantity=10),
        Inventory(_id="2", product_id="prod2", quantity=20),
    ]

    # Crear instancia del servicio con el repositorio mockeado
    service = GetAllInventoriesService(mock_repo)

    # Ejecutar el servicio
    result = service.execute()
 # Validar el resultado
    assert result.is_success  # Debe ser True en caso de éxito
    assert result.value is not None  # Validar que se devuelve una lista
    assert len(result.value) == 2  # Validar el número de inventarios devueltos
    assert result.value[0].product_id == "prod1"  # Validar los datos de un inventario

    # Validar que se llamó al método correcto del repositorio
    mock_repo.get_all.assert_called_once()