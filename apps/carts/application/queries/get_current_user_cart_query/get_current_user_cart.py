from typing import List
from core.application.services.application_service import Service
from core.application.results.result import Result
from .types.get_current_user_cart_response import GetCurrentUserCartResponse
from .types.get_current_user_cart_query import GetCurrentUserCartQuery
from ...exceptions.cart_not_found import CartNotFoundError
from ....domain.repositories.cart_repository import CartRepository


class GetCurrentUserCartService(Service[GetCurrentUserCartQuery, List[GetCurrentUserCartResponse]]):
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def execute(self, data: GetCurrentUserCartQuery):
        cart_id, products = self.cart_repository.get_cart_by_user(data.user_id)
        cart = self.cart_repository.get_cart_by_id(cart_id)

        if cart.is_archived:
            return Result[List[GetCurrentUserCartResponse]].make_failure(error = CartNotFoundError())
        if len(products) == 0: return Result[List[GetCurrentUserCartResponse]].make_success(value = {"cart_id": cart_id, "products": 0})
        
        if cart is None or not cart.order_id:
            cart.order_id = "Not assigned"

        list_of_products = []
        for product in products:
            item = GetCurrentUserCartResponse(
                cart_id = product.cart_id,
                product_id = product.product_id,
                price = product.unit_price,
                quantity = product.quantity
            )
            list_of_products.append(item)
        
        return Result[List[GetCurrentUserCartResponse]].make_success(value = list_of_products)