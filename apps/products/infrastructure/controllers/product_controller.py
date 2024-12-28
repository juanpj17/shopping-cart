from fastapi import APIRouter, Depends, HTTPException
from ..models.product_model import ProductModel
from ..repositories.postgre_product_repository import PostgreProductRepository
from ....auth.infrastructure.middlewares.verify_user_role import get_user
from ...application.commands.register_product_command.register_product import RegisterProductService
from .dto.register_product_dto import RegisterProductDto
from ...application.commands.update_product_command.update_product import UpdateProductService
from .dto.update_product_dto import UpdateProductDto
from ...application.commands.remove_product_command.remove_product import RemoveProductService
from .dto.remove_product_dto import RemoveProductDto
from ...application.queries.get_all_products_query.get_all_products import GetAllProductsService
from ...application.queries.get_product_by_id_query.get_product_by_id import GetProductByIdService
from .dto.get_product_by_id_dto import GetProductByIdDto
from ....inventories.application.commands.register_inventory_command.register_inventory import RegisterInventoryService
from ....inventories.infrastructure.repositories.posgre_inventory_repository import PostgreInventoryRepository
from ....inventories.infrastructure.models.inventory_model import InventoryModel

router = APIRouter(tags=['Products'])
product_model = ProductModel
inventory_model = InventoryModel
inventory_repository = PostgreInventoryRepository(inventory_model)
repository = PostgreProductRepository(product_model)

@router.get("/products")
def get_products():
    service = GetAllProductsService(repository)
    response = service.execute()
    return response.unwrap()

@router.get("/products/{product_id}")
def get_product(id: str):
    service = GetProductByIdService(repository)
    data = GetProductByIdDto(id = id)
    response = service.execute(data)
    return response.unwrap()

@router.post("/products")
def register_product(
    data: RegisterProductDto,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = RegisterProductService(repository)
    service.subscribe(RegisterInventoryService(inventory_repository))
    response = service.execute(data)
    return response.unwrap()

@router.put("/products/{product_id}")
def update_product(
    id: str,
    data: UpdateProductDto,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = UpdateProductService(repository)
    response = service.execute(id, data)
    return response.unwrap()

@router.delete("/products/{product_id}")
def delete_product(
    data: str,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = RemoveProductService(repository)
    response = service.execute(data)
    return response.unwrap()


