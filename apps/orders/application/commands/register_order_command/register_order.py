from apps.orders.domain.services.total_amount_domain_service import TotalOrderDomainService
from core.application.services.application_service import Service
from core.application.results.result import Result
from core.application.events.publisher import Publisher
from core.infrastructure.providers.uuid_service import UUIDService
from apps.carts.domain.repositories.cart_repository import CartRepository
from apps.carts.application.commands.update_cart_command.types.update_cart_command import UpdateCartCommand
from .types.register_order_command import RegisterOrderCommand
from ....domain.repositories.order_repository import OrderRepository
from ....domain.order import Order
from ....domain.order import StatusEnum

class RegisterOrderService(Service[RegisterOrderCommand ,str], Publisher[UpdateCartCommand]):

    def __init__(self, order_repository: OrderRepository, cart_repository: CartRepository):
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.uuid_service = UUIDService
        self.subscribers = []
        
    
    def execute(self, data: RegisterOrderCommand):
        _id = self.uuid_service.generate_id()
        total = 0
        products_in_cart = self.cart_repository.get_products_in_cart(data.cart_id)
        if len(products_in_cart) == 0: return Result[str].make_failure(value = {"cart_id": data.cart_id, "products": 0})
        total = TotalOrderDomainService().execute(products_in_cart)
        print("Total: ", total)
        order = Order(_id = _id, user_id = data.user_id, cart_id = data.cart_id, status = StatusEnum.PENDING, total = total)
        
        data_cart = UpdateCartCommand(cart_id = data.cart_id, order_id = _id, products = [])
        self.notify(data_cart)
        self.order_repository.save_order(order)
        return Result[str].make_success(value = _id)

        