from core.application.services.application_service import Service
from core.application.results.result import Result
from apps.inventories.domain.repositories.inventory_repository import InventoryRepository
from apps.carts.domain.repositories.cart_repository import CartRepository
from apps.inventories.domain.inventory import Inventory
from .types.update_order_command import UpdateOrderCommand
from ....domain.repositories.order_repository import OrderRepository
from ....domain.order import StatusEnum, Order

class UpdateOrderService(Service[UpdateOrderCommand, str]):
    def __init__(self, order_repository: OrderRepository, inventory_repository: InventoryRepository, cart_repository: CartRepository):
        self.inventory_repository = inventory_repository
        self.cart_repository = cart_repository
        self.order_repository = order_repository

    def execute(self, data: UpdateOrderCommand):
        order = self.order_repository.get_order_by_id(data.order_id)
        if data.status == "completed":
            cart_id, products_in_cart = self.cart_repository.get_cart_by_user(data.user_id)
            for product in products_in_cart: 
                product_inventory = self.inventory_repository.get_inventory_by_product(product.product_id)
                left_quantity = product_inventory.quantity - product.quantity
                inventory = Inventory(_id = product_inventory.entity_id, product_id = product.product_id, quantity = left_quantity)
                self.inventory_repository.save_inventory(inventory)
            order = Order(_id = data.order_id, user_id = data.user_id, cart_id = cart_id, status = StatusEnum.COMPLETED, total = order.total)
            self.cart_repository.archive_cart(cart_id)
            return Result[str].make_success(value = "Order completed")

        if data.status == "canceled":
            order = self.order_repository.get_order_by_id(data.order_id)
            cart_id, products_in_cart = self.cart_repository.get_cart_by_user(data.user_id)
            for product in products_in_cart: 
                self.cart_repository.remove_product(product.product_id)
        order = Order(_id = data.order_id, user_id = data.user_id, cart_id = cart_id, status = StatusEnum.CANCELLED, total = order.total)
        self.order_repository(order)
        