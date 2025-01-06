from unittest.mock import MagicMock
from core.application.results.result import Result
from apps.inventories.application.commands.update_inventory_command.update_inventory import UpdateInventoryService
from apps.inventories.application.commands.update_inventory_command.types.update_inventory_command import UpdateInventoryCommand
from apps.inventories.domain.inventory import Inventory
from apps.inventories.application.exceptions.inventory_not_found import InventoryNotFoundError

def test_update_inventory_success():
    # Crear un mock para el repositorio
    mock_repo = MagicMock()

    # Configurar el mock para devolver un inventario existente
    mock_repo.get_inventory_by_product.return_value = MagicMock(
        entity_id="inventory123",
        product_id="product123",
        quantity='10'
    )
     # Instanciar el servicio
    service = UpdateInventoryService(mock_repo)

    # Crear un comando de prueba
    command = UpdateInventoryCommand(product_id="product123", quantity='20')
    result = service.execute(command)
    assert result.is_success
    assert result.value == "product123"

    # Verificar que el repositorio guardó el inventario actualizado
    mock_repo.save_inventory.assert_called_once()
    saved_inventory = mock_repo.save_inventory.call_args[0][0]
    assert saved_inventory._id == "inventory123"
    assert saved_inventory.product_id == "product123"
    assert saved_inventory.quantity == '20'
    
def test_update_inventory_not_found():
    # Crear un mock para el repositorio
    mock_repo = MagicMock()

    # Configurar el mock para devolver None al buscar el inventario
    mock_repo.get_inventory_by_product.return_value = None

    # Instanciar el servicio
    service = UpdateInventoryService(mock_repo)

    # Crear un comando de prueba
    command = UpdateInventoryCommand(product_id="product123", quantity='20')

    # Ejecutar el método
    result = service.execute(command)

    # Verificar que el resultado sea un error
    assert result.is_failure
    assert isinstance(result.error, InventoryNotFoundError)

    # Verificar que no se intentó guardar ningún inventario
    mock_repo.save_inventory.assert_not_called()