from core.application.services.application_service import Service
from core.infrastructure.providers.uuid_service import UUIDService
from core.application.results.result import Result
from .types.register_cart_command import RegisterCartCommand
from ....domain.repositories.cart_repository import CartRepository
from ....domain.cart import Cart

class RegisterCartService(Service[RegisterCartCommand, str]):
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
        self.uuid_service = UUIDService

    def execute(self, data: RegisterCartCommand):
        _id = self.uuid_service.generate_id()
        cart = Cart(_id, data.user_id, None, None)
        self.cart_repository.save_cart(cart, products = None)
        return Result[str].make_success(value = _id)
