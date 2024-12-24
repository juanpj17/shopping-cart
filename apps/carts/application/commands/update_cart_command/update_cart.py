from apps.inventories.domain.repositories.inventory_repository import InventoryRepository
from apps.products.domain.repositories.product_repository import ProductRepository
from apps.products.application.exceptions.product_not_found import ProductNotFoundError
from core.application.services.application_service import Service
from core.application.results.result import Result
from core.infrastructure.providers.uuid_service import UUIDService
from .types.update_cart_command import UpdateCartCommand
from ...exceptions.not_enough_products import NotEnoughProductError
from ...exceptions.cart_not_found import CartNotFoundError
from ....domain.repositories.cart_repository import CartRepository
from ....domain.cart import Cart

class UpdateProductService(Service[UpdateCartCommand,str]):

    def __init__(
            self,
            cart_repository: CartRepository,
            product_repository: ProductRepository,
            inventory_repository: InventoryRepository 
        ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository
        self.inventory_repository = inventory_repository
        self.uuid_service = UUIDService

    def execute(self, data = UpdateCartCommand):
        res = self.cart_repository.get_cart_by_id(data.cart_id)
        cart = Cart(_id = data.cart_id, user_id = res.user_id, order_id = None, products = None)
        if not cart: return Result[str].make_failure(error = CartNotFoundError())

        list_of_products = []
        for item in data.products:
            product = self.product_repository.get_product_by_id(item.product_id) 
            if not product: return Result[str].make_failure(error = ProductNotFoundError())
            inventory = self.inventory_repository.get_inventory_by_product(item.product_id)

            if inventory.quantity - item.quantity < 0:
                return Result[str].make_failure(error = NotEnoughProductError(item.product_id)) 
            list_of_products.append(
                {
                    "id": self.uuid_service.generate_id(), 
                    "product_id": item.product_id, 
                    "unit_price": product.price, 
                    "quantity": item.quantity
                }
            )
        
        self.cart_repository.save_cart(cart, list_of_products)
        return Result[str].make_success(value="Cart updated successfully.")
