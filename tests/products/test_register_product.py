import pytest
from unittest.mock import MagicMock
from core.application.results.result import Result
from apps.products.application.commands.register_product_command.register_product import RegisterProductService
from apps.products.domain.product import Product
from apps.products.application.commands.register_product_command.types.product_command import ProductCommand
from core.infrastructure.providers.uuid_service import UUIDService
from apps.products.domain.services.calculate_product_price import CalculateProductPriceService

# Crear un mock de UUIDService
@pytest.fixture
def mock_uuid_service():
    mock = MagicMock(UUIDService)
    mock.generate_id.return_value = "f9060964-ac75-49e1-87df-b588ce739330"  # Simula un ID generado
    return mock
# Crear un mock del repositorio de productos
@pytest.fixture
def mock_product_repository():
    mock_repo = MagicMock()
    # Simular el método save_product para que no haga nada en realidad, pero se llame correctamente
    mock_repo.save_product.return_value = None  # No retornará nada
    return mock_repo
# Crear un mock de CalculateProductPriceService
@pytest.fixture
def mock_calculate_product_price_service():
    mock = MagicMock(CalculateProductPriceService)
    mock.execute.return_value = 100.0  # Simula que el precio calculado es 100.0
    return mock
# Crear un mock de Publisher (notify)
@pytest.fixture
def mock_publisher():
    return MagicMock()
# Test del servicio RegisterProductService
def test_register_product_service(mock_uuid_service, mock_product_repository, mock_calculate_product_price_service, mock_publisher):
    # Crear el servicio con las dependencias mockeadas
    service = RegisterProductService(product_repository=mock_product_repository)
    service.uuid_service = mock_uuid_service
    service.subscribers = [mock_publisher]  # Agregar mock de subscribers

    # Crear el comando de entrada (ProductCommand)
    product_command = ProductCommand()
    product_command.code="P001"
    product_command.name="Product 1"
    product_command.description="Description of product 1"
    product_command.cost=50.0
    product_command.margin=0.2
    product_command.status="active"
    # Ejecutar el servicio
    result = service.execute(product_command)

    # Verificar que el resultado sea exitoso
    assert result.is_success()  # Verifica que la operación fue exitosa
    assert result.unwrap() == "f9060964-ac75-49e1-87df-b588ce739330"  # Verifica que el ID generado es "1234"
    # Verificar que el UUIDService fue llamado para generar el ID
    mock_uuid_service.generate_id.assert_called_once()
     # Verificar que el producto fue guardado en el repositorio
    mock_product_repository.save_product.assert_called_once()
   