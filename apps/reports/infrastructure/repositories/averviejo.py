import sqlalchemy
from apps.reports.domain.product_sales_report import ProductSalesReport
from core.infrastructure.db_session.postgre_session import DBSession
from sqlmodel import cast, select, func, desc
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
    def __init__(self, order_model: OrderModel, product_model: ProductModel, cart_model: CartModel, product_cart_model: ProductCartModel, user_model: UserModel):
        self.session = DBSession.get_session()
        self.order_model = order_model
        self.product_model = product_model
        self.cart_model = cart_model
        self.product_cart_model = product_cart_model
        self.user_model = user_model

# VENTAS TOTALES
    def get_total_sales(self):
        statement = select(func.count(OrderModel.entity_id).label("sales")).where(OrderModel.status == 'completed')
        result = self.session.exec(statement).first()
        return result
    
    def get_total_sales_amount(self):
        statement = (
            select(func.sum(cast(OrderModel.total, sqlalchemy.Numeric)).label("total")) 
            .where(OrderModel.status == 'completed')
        )
        result = self.session.exec(statement).first()
        return result
    
    def get_sales_by_products(self):
        statement = (
            select(
                ProductModel.name,
                func.sum(ProductCartModel.quantity).label("quantity"),
                func.sum(ProductCartModel.unit_price * ProductCartModel.quantity).label("amount"),
            )
            .join(CartModel, CartModel.entity_id == ProductCartModel.cart_id)
            .join(OrderModel, OrderModel.cart_id == CartModel.entity_id)
            .join(ProductModel, ProductModel.entity_id == ProductCartModel.product_id)
            .where(OrderModel.status == "completed")
            .group_by(ProductModel.name)
        )
        results = self.session.exec(statement).all()
        return [ProductSalesReport(name=row[0], quantity=row[1], amount=row[2]) for row in results]
    
    

# GANANCIAS TOTALES
    def get_total_profit(self):
        statement = select( func.sum(ProductModel.price - ProductModel.cost).label("profits"))
        response = self.session.exec(statement).first()
        return response
    
# GANANCIAS DE PRODUCTO POR ID
    def get_product_profit_by_id(self, id): 
        statement = (
            select(
                ProductModel.name,
                func.sum(ProductCartModel.quantity).label("quantity"),
                func.sum(ProductCartModel.unit_price * ProductCartModel.quantity).label("amount"),
            )
            .join(CartModel, CartModel.entity_id == ProductCartModel.cart_id)
            .join(OrderModel, OrderModel.cart_id == CartModel.entity_id)
            .join(ProductModel, ProductModel.entity_id == ProductCartModel.product_id)
            .where(OrderModel.status == "completed")
            .where(ProductModel.entity_id == id)
            .group_by(ProductModel.name)
        )
        results = self.session.exec(statement).all()
        return [ProductSalesReport(name=row[0], quantity=row[1], amount=row[2]) for row in results]

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