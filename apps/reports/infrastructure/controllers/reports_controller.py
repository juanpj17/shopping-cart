from fastapi import APIRouter, Depends, HTTPException
from apps.auth.infrastructure.middlewares.verify_user_role import get_user

from apps.reports.application.queries.report_product_profit.report_product_profit_by_id import GetProductProfitsById
from apps.reports.application.queries.report_product_sales.report_product_sales_by_id import GetProductSalesById
from apps.reports.application.queries.report_top_products.report_top_products import GetTopProducts
from apps.reports.application.queries.report_top_users.report_top_users import GetTopUsers
from apps.reports.application.queries.report_total_profit.report_total_profit import GetTotalProfits
from apps.reports.application.queries.report_total_sales.report_total_sales import GetTotalSales

from ..controllers.types.product_profit_by_id_dto import ProductProfitByIdDto
from ..controllers.types.product_sales_by_id_dto import ProductSalesByIdDto

from apps.reports.infrastructure.repositories.postgre_reports_repository import PostgreReportsRepository
from apps.carts.infrastructure.models.cart_model import CartModel, ProductCartModel
from apps.carts.infrastructure.repositories.postgre_cart_repository import PostgreCartRepository
from apps.orders.infrastructure.models.order_model import OrderModel
from apps.orders.infrastructure.repositories.postgre_order_repository import PostgreOrderRepository
from apps.products.infrastructure.models.product_model import ProductModel
from apps.products.infrastructure.repositories.postgre_product_repository import PostgreProductRepository
from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.repositories.postgres_user_repository import PostgreUserRepository


router = APIRouter(tags=['Reports'])
order_repository = PostgreOrderRepository(OrderModel)
cart_repository = PostgreCartRepository(CartModel, ProductCartModel)
product_repository = PostgreProductRepository(ProductModel)
user_repository = PostgreUserRepository(UserModel)
report_repository = PostgreReportsRepository(OrderModel, ProductModel, CartModel, ProductCartModel, UserModel)


# VENTAS TOTALES
@router.get('/reports/sales/total')
def get_total_sales(
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetTotalSales(report_repository)
    response = service.execute()
    if response.is_success():
        return response.value
    else:
        raise HTTPException(status_code=404, detail="No sales found.")

# VENTAS DE PRODUCTO POR ID
@router.get('/reports/sales/{product_id}')
def get_product_sales_by_id(
    product_id: str, 
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetProductSalesById(report_repository)
    response = service.execute(product_id)
    return response.unwrap()

# GANANCIAS TOTALES
@router.get('/reports/profit/total')
def get_total_profit(
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetTotalProfits(report_repository)
    response = service.execute()
    return response.unwrap()

# GANANCIAS DE PRODUCTO POR ID
@router.get('/reports/profit/{product_id}')
def get_product_profit_by_id(
    product_id: str, 
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetProductProfitsById(report_repository)
    response = service.execute(product_id)
    return response.unwrap()

# PRODUCTOS TOP
@router.get('/reports/products/top')
def get_top_products(
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetTopProducts(report_repository)
    response = service.execute()
    return response.unwrap()

# USUARIOS TOP
@router.get('/reports/customers/top')
def get_top_users(
    user: dict = Depends(get_user)
):
    if user.get("role") not in ["Superadmin", "Manager"]:
        raise HTTPException(status_code = 403, detail = "Forbbiden endpoint")
    service = GetTopUsers(report_repository)
    response = service.execute()
    return response.unwrap()