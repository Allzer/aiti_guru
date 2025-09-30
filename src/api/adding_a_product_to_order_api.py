from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/adding_a_product_to_order",
    tags=["clients"]
)

@router.get('/')
def get_order():
    pass