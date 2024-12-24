from core.application.services.application_service import Service
from core.application.results.result import Result
from .types.remove_product_from_cart_command import RemoveProductFromCartCommand
from ....domain.repositories.cart_repository import CartRepository

class RemoveProductFromCartService(Service[RemoveProductFromCartCommand, str]):
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self, data: RemoveProductFromCartCommand):
        cart_id, products = self.cart_repository.get_cart_by_user(data.user_id)
        if len(products) == 0: return Result[str].make_success(value = {"cart_id": cart_id, "products": 0})
        self.cart_repository.remove_product(data.product_id)
        return Result[str].make_success(value = "Product deletedc")
        