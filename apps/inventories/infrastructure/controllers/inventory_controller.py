from fastapi import APIRouter, Depends, HTTPException
from ..models.inventory_model import InventoryModel
from ..repositories.posgre_inventory_repository import PostgreInventoryRepository
from ...application.commands.update_inventory_command.update_inventory import UpdateInventoryService
from .types.update_inventory_dto import UpdateInventoryDto
from ....auth.infrastructure.middlewares.verify_user_role import get_user
from ...application.queries.get_all_inventories_query.get_all_inventories import GetAllInventoriesService
from ...application.queries.get_inventory_by_product.get_inventory_by_product import GetInventoryByProductService
from .types.get_inventory_by_product_dto import GetInventoryByProductDto

router = APIRouter(tags=['Inventories'])
inventory_model = InventoryModel
repository = PostgreInventoryRepository(inventory_model)

@router.put("/inventories/update")
def update_inventory(
    data: UpdateInventoryDto,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = UpdateInventoryService(repository)
    response = service.execute(data)
    return response.unwrap()

@router.get("/inventories")
def get_all(user: dict = Depends(get_user)):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetAllInventoriesService(repository)
    response = service.execute()
    return response.unwrap()

@router.get("/inventories/{product_id}")
def get_inventory_by_product(
    product_id: str,
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetInventoryByProductService(repository)
    data = GetInventoryByProductDto(product_id = product_id)
    response = service.execute(data)
    return response.unwrap()