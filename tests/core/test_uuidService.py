from core.infrastructure.providers import uuid_service
from unittest.mock import patch
import uuid


def test_generate_id_mocked():
    # Arrange
    mock_uuid = "123e4567-e89b-12d3-a456-426614174000"
    service = uuid_service.UUIDService  # Instanciamos la clase
    
    # Usamos mock para simular uuid.uuid4()
    with patch('uuid.uuid4', return_value=uuid.UUID(mock_uuid)):
        # Act
        generated_id = service.generate_id()  # Llamamos al método de instancia

        # Assert
        assert generated_id == mock_uuid  # El ID generado debe ser el mockeado
