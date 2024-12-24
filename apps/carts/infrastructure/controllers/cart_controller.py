from fastapi import APIRouter, Depends
from apps.products.infrastructure.models.product_model import ProductModel
from apps.products.infrastructure.repositories.postgre_product_repository import PostgreProductRepository
from apps.inventories.infrastructure.models.inventory_model import InventoryModel
from apps.inventories.infrastructure.repositories.posgre_inventory_repository import PostgreInventoryRepository
from .dtos.register_cart_dto import RegisterCartDto
from .dtos.update_cart_dto import UpdateCartDto
from .dtos.remove_product_from_cart import RemoveProductFromCartDto
from .dtos.get_current_user_cart_dto import GetCurrentUserCartDto
from ..models.cart_model import CartModel, ProductCartModel
from ..repositories.postgre_cart_repository import PostgreCartRepository
from ...application.commands.register_cart_command.register_cart import RegisterCartService
from ...application.commands.update_cart_command.update_cart import UpdateProductService
from ...application.queries.get_current_user_cart_query.get_current_user_cart import GetCurrentUserCartService
from ...application.commands.remove_product_from_cart_command.remove_product_from_cart import RemoveProductFromCartService
from ....auth.infrastructure.middlewares.verify_user_role import get_user


router = APIRouter(tags=['Carts'])
cart_model = CartModel
product_cart_model = ProductCartModel
product_model = ProductModel
inventory_model = InventoryModel
repository = PostgreCartRepository(cart_model, product_cart_model)
product_repository = PostgreProductRepository(product_model)
inventory_repository = PostgreInventoryRepository(inventory_model)



@router.post("/carts/register")
def register_cart(user: dict = Depends(get_user)):
    data = RegisterCartDto(user_id = user.get("id"))
    service = RegisterCartService(repository)
    response = service.execute(data)
    return response.unwrap()

@router.put("/carts/add/product")
def update_cart(
    data: UpdateCartDto,
    user: dict = Depends(get_user)
):
    service = UpdateProductService(repository, product_repository, inventory_repository)
    response = service.execute(data)
    return response.unwrap()

@router.get("/carts/get")
def get_cart(
    user: dict = Depends(get_user)
):
    service = GetCurrentUserCartService(repository)
    data = GetCurrentUserCartDto( user_id = user.get("id"))
    response = service.execute(data)
    return response.unwrap()


@router.delete("/carts/{product_id}")
def get_cart(
    product_id: str,
    user: dict = Depends(get_user)
):
    service = RemoveProductFromCartService(repository)
    data = RemoveProductFromCartDto(product_id = product_id, user_id = user.get("id"))
    response = service.execute(data)
    return response.unwrap()