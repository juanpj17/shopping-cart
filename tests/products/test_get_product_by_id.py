import pytest
from unittest.mock import MagicMock
from apps.products.application.queries.get_product_by_id_query.get_product_by_id import GetProductByIdQuery
from apps.products.domain.product import Product
from core.application.results.result import Result
from apps.products.application.exceptions.product_not_found  import ProductNotFoundError
from apps.products.application.queries.get_product_by_id_query.types.product_response import GetProductByIdResponse
from apps.products.application.queries.get_product_by_id_query.types.product_query import GetProductByIdQuery
from apps.products.application.queries.get_product_by_id_query.get_product_by_id import GetProductByIdService
# Prueba exitosa de GetProductByIdService

# Arrange
def test_get_product_by_id_service_success():
    # Crear el query de entrada
    query = GetProductByIdQuery()
    query.id = "1"
    
    # Crear una respuesta simulada del repositorio
    mock_product = MagicMock()
    mock_product._id = "1"
    mock_product.code = "P001"
    mock_product.name = "Product 1"
    mock_product.description = "Description of Product 1"
    mock_product.price = 100.0
    mock_product.cost = 50.0
    mock_product.margin = 50.0

    # Crear un mock del repositorio
    mock_product_repository = MagicMock()
    mock_product_repository.get_product_by_id.return_value = mock_product

    # Instanciar el servicio con el repositorio simulado
    service = GetProductByIdService(product_repository=mock_product_repository)

    # Act
    # Ejecutar el servicio
    result = service.execute(query)

    # Assert
    # Verificar que el resultado es exitoso
    assert result.is_success()
    assert result.value.id == "1"
    assert result.value.code == "P001"
    assert result.value.name == "Product 1"
    assert result.value.price == 100.0

