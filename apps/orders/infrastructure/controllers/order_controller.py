from fastapi import APIRouter, Depends, HTTPException
from apps.auth.infrastructure.middlewares.verify_user_role import get_user
from apps.carts.infrastructure.models.cart_model import CartModel
from apps.carts.infrastructure.models.cart_model import ProductCartModel
from apps.carts.infrastructure.repositories.postgre_cart_repository import PostgreCartRepository
from apps.carts.application.commands.update_cart_command.update_cart import UpdateProductService
from apps.products.infrastructure.models.product_model import ProductModel
from apps.products.infrastructure.repositories.postgre_product_repository import PostgreProductRepository
from apps.inventories.infrastructure.models.inventory_model import InventoryModel
from apps.inventories.infrastructure.repositories.posgre_inventory_repository import PostgreInventoryRepository
from .dtos.register_order_dto import RegisterOrderDto
from .dtos.update_order_dto import UpdateOrderDto
from .dtos.get_order_by_id_dto import GetOrderByIdDto
from ..models.order_model import OrderModel
from ..repositories.postgre_order_repository import PostgreOrderRepository
from ...application.commands.register_order_command.register_order import RegisterOrderService
from ...application.commands.update_order_command.update_order import UpdateOrderService
from ...application.queries.get_all_orders_query.get_all_orders import GetAllOrdersServices
from ...application.queries.get_order_by_id_query.get_order_by_id import GetOrderByIdService

router = APIRouter(tags=['Orders'])
order_repository = PostgreOrderRepository(OrderModel)
cart_repository = PostgreCartRepository(CartModel, ProductCartModel)
product_repository = PostgreProductRepository(ProductModel)
inventory_repository = PostgreInventoryRepository(InventoryModel)

@router.post("/orders/{cart_id}")
def register_order(
    cart_id: str,
    user: dict = Depends(get_user)
):
    data = RegisterOrderDto(cart_id = cart_id, user_id = user.get("id"))
    service = RegisterOrderService(order_repository, cart_repository)
    service.subscribe(UpdateProductService(cart_repository,product_repository, inventory_repository))
    response = service.execute(data)
    return response.unwrap()

@router.put("/orders/")
def update_order(
    data: UpdateOrderDto,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint") 
    service = UpdateOrderService(order_repository, inventory_repository, cart_repository)
    response = service.execute(data)
    return response.unwrap()

@router.get("/orders")
def get_all_orders(
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint") 
    service = GetAllOrdersServices(order_repository)
    response = service.execute()
    return response.unwrap()

@router.get("/orders/{order_id}")
def get_order_by_id(
    order_id: str,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint") 
    data = GetOrderByIdDto(order_id = order_id)
    service = GetOrderByIdService(order_repository)
    response = service.execute(data)
    return response.unwrap()