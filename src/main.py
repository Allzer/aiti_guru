from fastapi import FastAPI

from src.api.adding_a_product_to_order_api import router as router

app = FastAPI()

app.include_router(router)

from src import api