from typing import List
from core.application.services.application_service import Service
from core.application.results.result import Result
from ...exceptions.orders_not_found import OrdersNotFoundError
from ....domain.repositories.order_repository import OrderRepository
from ....domain.order import Order

class GetAllOrdersServices(Service[None, List[Order]]):
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def execute(self):
        orders = self.order_repository.get_all_orders()
        if len(orders) == 0: Result[List[Order]].make_failure(error = OrdersNotFoundError())

        list_of_orders = []
        for item in orders:
            order = Order(item.entity_id, item.user_id, item.cart_id, item.status, item.total)
            list_of_orders.append(order)

        return Result[List[Order]].make_success(value = list_of_orders)
        