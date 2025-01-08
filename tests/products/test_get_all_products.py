import pytest
from unittest.mock import MagicMock
from apps.products.application.queries.get_all_products_query.get_all_products import GetAllProductsService
from apps.products.domain.product import Product
from core.application.results.result import Result
from apps.products.application.exceptions.products_not_found import ProductsNotFoundError

# Arrange
def test_get_all_products_service_success():
    # Crear una lista simulada de productos con la nueva estructura
    mock_products = [
        Product(_id="1", code="P001", name="Product 1", description="Description 1", price=100.0, cost=50.0, margin=50.0, status="Available"),
        Product(_id="2", code="P002", name="Product 2", description="Description 2", price=200.0, cost=100.0, margin=100.0, status="Out of stock"),
    ]
    
    # Crear un mock del repositorio
    mock_product_repository = MagicMock()
    mock_product_repository.get_all_products.return_value = mock_products

    # Instanciar el servicio con el repositorio simulado
    service = GetAllProductsService(product_repository=mock_product_repository)

    # Act
    # Ejecutar el servicio
    result = service.execute()

    # Assert
    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert len(result.value) == 2
    assert result.value[0].name == "Product 1"
    assert result.value[1].name == "Product 2"

# Arrange
def test_get_all_products_service_no_products_found():
    # Crear un mock del repositorio que retorna una lista vacía
    mock_product_repository = MagicMock()
    mock_product_repository.get_all_products.return_value = []

    # Instanciar el servicio con el repositorio simulado
    service = GetAllProductsService(product_repository=mock_product_repository)

    # Act
    # Ejecutar el servicio
    result = service.execute()

    # Assert
    # Verificar que el resultado es un fallo
    assert result.is_failure()
    assert isinstance(result.error, ProductsNotFoundError)
    assert result.error.message == 'Products not found'