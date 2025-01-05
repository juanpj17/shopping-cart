from core.infrastructure.db_session.postgre_session import DBSession
from sqlmodel import select, func, desc
from sqlalchemy.exc import SQLAlchemyError
from ...application.domain.repositories.reports_repository import ReportsRepository
# Models
from ....carts.infrastructure.models.cart_model import CartModel
from ....carts.infrastructure.models.cart_model import ProductCartModel
from ....orders.infrastructure.models.order_model import OrderModel
from ....products.infrastructure.models.product_model import ProductModel
from ....users.infrastructure.models.user_model import UserModel


#  profit = price - cost

# order status enum:
# PENDING = "pending"
# COMPLETED = "completed"
# CANCELLED = "cancelled"

class PostgreReportsRepository(ReportsRepository):
    def __init__(self):
        self.session = DBSession.get_session()

# VENTAS TOTALES
    def get_total_sales(self):
        statement = select(func.count(OrderModel.entity_id).label("sales")).where(OrderModel.status == 'completed')
        response = self.session.exec(statement)
        return response

# GANANCIAS TOTALES
    def get_total_profit(self):
        statement = select( func.sum(ProductModel.price - ProductModel.cost).label("profits"))
        response = self.session.exec(statement).first()
        return response
    
# GANANCIAS DE PRODUCTO POR ID
    def get_product_profit_by_id(self, id): 
        statement = select((ProductModel.price - ProductModel.cost).label("product_profit")).where(ProductModel.entity_id == id)
        response = self.session.exec(statement).first()
        return response

# VENTAS DE PRODUCTO POR ID
    def get_product_sales_by_id(self, id): #requires JOINS FROM order.status = completed, products, cart
        statement = select(ProductModel.entity_id, func.count(ProductCartModel.product_id).label("sales")).where(ProductCartModel.product_id == id, 
                                                                                                                 ProductCartModel.cart_id == CartModel.entity_id, 
                                                                                                                 CartModel.order_id == OrderModel.entity_id, 
                                                                                                                 OrderModel.status == 'completed', 
                                                                                                                 ProductModel.entity_id == id).group_by(ProductModel.entity_id)
                                                                                                   
        response = self.session.exec(statement)
        return response


# PRODUCTOS TOP
    def get_top_products(self): #requires JOINS FROM order.status = completed, products, cart
        statement = select(ProductModel.entity_id, func.count(OrderModel.entity_id).label("sales")).where(ProductCartModel.product_id == ProductModel.entity_id, 
                                                                                            ProductCartModel.cart_id == CartModel.entity_id,
                                                                                            CartModel.order_id == OrderModel.entity_id, 
                                                                                            OrderModel.status == 'completed').group_by(ProductModel.entity_id).order_by(ProductModel.entity_id, desc("sales"))
        response = self.session.exec(statement)
        return response

# USUARIOS TOP
    def get_top_users(self): #requires JOINS FROM order.status = completed, users
        statement = select(UserModel.entity_id, func.count(OrderModel.entity_id).label("purchases")).where(OrderModel.user_id == UserModel.entity_id, 
                                                                                                           OrderModel.status == 'completed').group_by(UserModel.entity_id).order_by(UserModel.entity_id, desc("purchases"))
        response = self.session.exec(statement)
        return response