from fastapi import FastAPI
from apps.users.infrastructure.controllers.user_controller import router as user_router
from apps.products.infrastructure.controllers.product_controller import router as product_router
from apps.inventories.infrastructure.controllers.inventory_controller import router as inventory_router
from apps.carts.infrastructure.controllers.cart_controller import router as cart_router
from apps.orders.infrastructure.controllers.order_controller import router as order_router
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(cart_router)
app.include_router(order_router)