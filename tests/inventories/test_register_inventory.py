import pytest
from unittest.mock import MagicMock, patch
from apps.inventories.application.commands.register_inventory_command.register_inventory import RegisterInventoryService
from apps.inventories.application.commands.register_inventory_command.types.register_inventory_command import RegisterInventoryCommand
from apps.inventories.domain.inventory import Inventory
from core.infrastructure.providers.uuid_service import UUIDService

def test_register_inventory_service_without_explicit_repo():
    # Crear un mock genérico para el repositorio
    mock_repo = MagicMock()
    # Mockear el servicio UUID para que devuelva un valor específico
    with patch.object(UUIDService, 'generate_id', return_value="generated-uuid") as mock_uuid_service:
        # Instanciar el servicio usando el mock del repositorio
        service = RegisterInventoryService(mock_repo)
     # Crear un comando de prueba
        command = RegisterInventoryCommand(product_id="product123")
         # Ejecutar el método
        service.execute(command)
          # Verificar que UUIDService.generate_id fue llamado
        mock_uuid_service.assert_called_once()
         # Obtener el objeto que fue llamado con save_inventory
        saved_inventory = mock_repo.save_inventory.call_args[0][0]
        
        # Verificar que los atributos coinciden
        assert saved_inventory._id == "generated-uuid"
        assert saved_inventory.product_id == "product123"
        assert saved_inventory.quantity == 0
        
def test_register_inventory_service_update_without_explicit_repo():
    # Crear un mock genérico para el repositorio
    mock_repo = MagicMock()
    
    # Mockear el servicio UUID
    with patch.object(UUIDService, 'generate_id', return_value="generated-uuid"):
        # Instanciar el servicio usando el mock del repositorio
        service = RegisterInventoryService(mock_repo)
     # Crear un comando de prueba
        command = RegisterInventoryCommand(product_id="product123")
        
        # Mockear el método execute
        service.execute = MagicMock()
        
        # Llamar al método update
        service.update(command)
        
        # Verificar que execute fue llamado correctamente
        service.execute.assert_called_once_with(command)


       