from typing import Dict, Optional, List
from sqlmodel import select, delete, update, SQLModel
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from core.infrastructure.db_session.postgre_session import DBSession
from ...domain.repositories.cart_repository import CartRepository
from ..models.cart_model import CartModel
from ..models.cart_model import ProductCartModel
from ...domain.cart import Cart

class PostgreCartRepository(CartRepository):
    
    def __init__(self, cart_model: SQLModel, product_cart_model: SQLModel):
        self.cart_model = cart_model
        self.product_cart_model = ProductCartModel
        self.session = DBSession.get_session()

    def save_cart(self, cart: Cart | None, products: Optional[List[Dict]]):
        try:
            existing_cart = self.get_cart_by_id(cart._id)

            if not existing_cart:
                new_cart = CartModel(
                    entity_id = cart._id,
                    user_id = cart.user_id,
                    order_id = cart.order_id,
                    created_at = datetime.now()
                )

                self.session.add(new_cart)
    
            if products:
                for product in products:
                    new_product_cart = ProductCartModel(
                        id = product.get("id"),
                        cart_id = cart._id,
                        product_id = product.get("product_id"),
                        quantity = product.get("quantity"),
                        unit_price = product.get("unit_price"),
                        created_at = datetime.now()
                    )
                    self.session.add(new_product_cart)

            if cart.order_id: existing_cart.order_id = cart.order_id
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RuntimeError(f"Error saving the inventory: {e}")


    def get_cart_by_id(self, id):
        statement = select(CartModel).where(CartModel.entity_id == id)
        response = self.session.exec(statement).first()
        return response
    
    def get_cart_by_user(self, id: str):
        statement = select(CartModel).where(
            (CartModel.user_id == id) & (CartModel.is_archived == False)  
        )
        response = self.session.exec(statement).first()
        
        statement = select(ProductCartModel).where(ProductCartModel.cart_id == response.entity_id)
        res = self.session.exec(statement).all()
        return response.entity_id, res

    def get_products_in_cart(self, id: str):
        statement = select(ProductCartModel).where(ProductCartModel.cart_id == id)
        response = self.session.exec(statement).all()
        return response
    
    def remove_product(self, id: str):
        statement = delete(ProductCartModel).where(ProductCartModel.product_id == id)
        self.session.exec(statement)
        self.session.commit()
        
    def archive_cart(self, cart_id: str):
        try:
            statement = update(CartModel).where(CartModel.id == cart_id).values(is_archived=True)
            self.session.exec(statement)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Error archiving cart with ID {cart_id}: {e}")