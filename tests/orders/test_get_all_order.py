from unittest.mock import MagicMock
from apps.orders.application.queries.get_all_orders_query.get_all_orders import GetAllOrdersServices
from apps.orders.domain.order import Order, StatusEnum
from core.application.results.result import Result
from apps.orders.application.exceptions.orders_not_found import OrdersNotFoundError


def test_get_all_orders_service_success():
    # Crear órdenes simuladas con el nuevo modelo
    mock_orders = [
    MagicMock(entity_id="1", user_id="user1", cart_id="cart1", status=StatusEnum.PENDING, total=100.0),
    MagicMock(entity_id="2", user_id="user2", cart_id="cart2", status=StatusEnum.COMPLETED, total=200.0),
]

    # Simular el repositorio
    mock_order_repository = MagicMock()
    mock_order_repository.get_all_orders.return_value = mock_orders
     # Crear instancia del servicio
    get_all_orders_service = GetAllOrdersServices(order_repository=mock_order_repository)

    # Ejecutar el servicio
    result = get_all_orders_service.execute()

    # Verificaciones
    assert result.is_success()
    assert isinstance(result.value, list)
    assert len(result.value) == len(mock_orders)
    for i, order in enumerate(result.value):
        assert order._id == mock_orders[i].entity_id
        assert order.user_id == mock_orders[i].user_id
        assert order.cart_id == mock_orders[i].cart_id
        assert order.status == mock_orders[i].status
        assert order.total == mock_orders[i].total

    # Verificar que el método del repositorio fue llamado una vez
    mock_order_repository.get_all_orders.assert_called_once()

def test_get_all_orders_service_failure():
    # Simular que no hay órdenes en el repositorio
    mock_order_repository = MagicMock()
    mock_order_repository.get_all_orders.return_value = []  # Devuelve una lista vacía

    # Crear instancia del servicio
    get_all_orders_service = GetAllOrdersServices(order_repository=mock_order_repository)

    # Ejecutar el servicio
    result = get_all_orders_service.execute()

    # Verificaciones
    assert result.is_failure()  # El resultado debe ser un fallo
    assert isinstance(result.error, OrdersNotFoundError)  # El error debe ser de tipo OrdersNotFoundError
    assert result.error.message == "Orders not found" 