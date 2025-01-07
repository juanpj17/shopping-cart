from core.application.services.application_service import Service
from core.application.results.result import Result
from .types.get_order_by_id_query import GetOrderByIdQuery
from ...exceptions.order_not_found import OrderNotFoundError
from ....domain.repositories.order_repository import OrderRepository
from ....domain.order import Order

class GetOrderByIdService(Service[GetOrderByIdQuery, Order]):
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def execute(self, data: GetOrderByIdQuery):
        order = self.order_repository.get_order_by_id(data.order_id)
        if not order: return Result[Order].make_failure(error = OrderNotFoundError())
        order = Order(order.entity_id, order.user_id, order.cart_id, order.status, order.total)

        return Result[Order].make_success(value = order)
        