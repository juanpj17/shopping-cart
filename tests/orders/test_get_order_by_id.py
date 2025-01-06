from unittest.mock import MagicMock
from apps.orders.application.queries.get_order_by_id_query.get_order_by_id import GetOrderByIdService
from apps.orders.domain.order import Order, StatusEnum
from core.application.results.result import Result
from apps.orders.application.queries.get_order_by_id_query.types.get_order_by_id_query import GetOrderByIdQuery
from apps.orders.domain.repositories.order_repository import OrderRepository
from apps.orders.application.exceptions.order_not_found import OrderNotFoundError

def test_get_order_by_id_service_success():
    # Simulamos una orden existente que el repositorio devolverá
    mock_order_repository = MagicMock()
    mock_order = MagicMock()
    mock_order.entity_id = "1"
    mock_order.user_id = "user_123"
    mock_order.cart_id = "cart_456"
    mock_order.status = StatusEnum.PENDING
    mock_order.total = 100.0

    mock_order_repository.get_order_by_id.return_value = mock_order  # Simula la respuesta del repositorio

    # Crear la consulta
    query = GetOrderByIdQuery(order_id="1")

    # Crear la instancia del servicio
    get_order_by_id_service = GetOrderByIdService(order_repository=mock_order_repository)

    # Ejecutar el servicio
    result = get_order_by_id_service.execute(query)

    # Verificaciones
    assert result.is_success()  # El resultado debe ser un éxito
    assert result.value._id == "1"  # Comprobamos que el ID de la orden sea correcto
    assert result.value.user_id == "user_123"  # Verificamos que el ID del usuario sea correcto
    assert result.value.status == StatusEnum.PENDING  # Verificamos el estado
    assert result.value.total == 100.0  # Verificamos el total

    # Verificamos que el repositorio fue llamado con el ID correcto
    mock_order_repository.get_order_by_id.assert_called_once_with("1")

def test_get_order_by_id_service_failure():
    # Simulamos que no se encuentra la orden en el repositorio
    mock_order_repository = MagicMock()
    mock_order_repository.get_order_by_id.return_value = None  # Simulacion que no se encuentra la orden

    # Crear la consulta
    query = GetOrderByIdQuery(order_id="1")

    # Crear la instancia del servicio
    get_order_by_id_service = GetOrderByIdService(order_repository=mock_order_repository)

    # Ejecutar el servicio
    result = get_order_by_id_service.execute(query)

    # Verificaciones
    assert result.is_failure()  # El resultado debe ser un fallo
    assert isinstance(result.error, OrderNotFoundError)  # El error debe ser de tipo OrderNotFoundError

  