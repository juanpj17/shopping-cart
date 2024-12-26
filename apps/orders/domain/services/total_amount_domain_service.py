from apps.carts.infrastructure.models.cart_model import ProductCartModel
from core.domain.services.domain_service import DomainService


class TotalOrderDomainService(DomainService[ProductCartModel ,float]):

    def execute(self, data: ProductCartModel) -> float:
        total = 0
        for product in data:
            total += product.unit_price * product.quantity
        return total