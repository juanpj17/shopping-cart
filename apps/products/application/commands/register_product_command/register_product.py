from core.application.services.application_service import Service
from .types.product_command import ProductCommand
from ....domain.repositories.product_repository import ProductRepository
from core.infrastructure.providers.uuid_service import UUIDService
from ....domain.product import Product
from core.application.results.result import Result
from ....domain.services.calculate_product_price import CalculateProductPriceService
from core.application.events.publisher import Publisher
from .....inventories.application.commands.register_inventory_command.types.register_inventory_command import RegisterInventoryCommand 

class RegisterProductService(Service[ProductCommand, str], Publisher[RegisterInventoryCommand]):

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.uuid_service = UUIDService
        self.subscribers = []

    def execute(self, data: ProductCommand):
        id = self.uuid_service.generate_id()
        # code = self.uuid_service.generate_id()
        service = CalculateProductPriceService()
        price = service.execute({"cost": data.cost, "margin": data.margin})
        product = Product(
            _id = id,
            code = data.code,
            name = data.name,
            description = data.description,
            price = price,
            cost = data.cost,
            margin = data.margin,
            status = data.status
        )

        product_id = RegisterInventoryCommand(product_id = id)
        self.product_repository.save_product(product)
        self.notify(product_id)
        return Result[str].make_success(value=id)