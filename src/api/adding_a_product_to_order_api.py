from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.api.schemas import OrderItemResponse
from database import SessionDep
from src.models.models_for_tz import Order, Product, OrderItem
    
from fastapi.responses import HTMLResponse

router = APIRouter()

class AddItemRequest(BaseModel):
    product_id: UUID
    quantity: PositiveInt

@router.post("/orders/{order_id}/items", status_code=status.HTTP_201_CREATED)
async def add_item_to_order(
    order_id: UUID,
    body: AddItemRequest,
    session: SessionDep,
):
    """
    Добавляет товар в заказ:
      - если позиция уже есть — увеличивает quantity,
      - если нет на складе — возвращает 409 Conflict.
    Возвращает json с деталями позиции (order_id, product_id, quantity, price_at_order, product_name).
    """
    try:
        async with session.begin():
            q = select(Order).where(Order.id == order_id)
            res = await session.execute(q)
            order = res.scalar_one_or_none()
            if order is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

            q2 = select(Product).where(Product.id == body.product_id).with_for_update()
            res2 = await session.execute(q2)
            product: Optional[Product] = res2.scalar_one_or_none()
            if product is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

            if product.stock_quantity < int(body.quantity):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Not enough stock. Requested {body.quantity}, available {product.stock_quantity}"
                )

            q3 = select(OrderItem).where(
                OrderItem.order_id == order_id,
                OrderItem.product_id == body.product_id
            )
            res3 = await session.execute(q3)
            order_item: Optional[OrderItem] = res3.scalar_one_or_none()

            if order_item is None:
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=body.product_id,
                    quantity=int(body.quantity),
                    price_at_order=product.price,
                )
                session.add(order_item)
                created = True
            else:
                order_item.quantity = order_item.quantity + int(body.quantity)
                session.add(order_item)
                created = False

            product.stock_quantity = product.stock_quantity - int(body.quantity)
            session.add(product)

            await session.flush()
            await session.refresh(order_item)

        return {
            "order_id": str(order_item.order_id),
            "product_id": str(order_item.product_id),
            "quantity": int(order_item.quantity),
            "price_at_order": float(order_item.price_at_order),
            "product_name": getattr(order_item, "product", None).name if getattr(order_item, "product", None) else None,
            "created": created
        }
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

@router.get("/", response_class=HTMLResponse)
async def read_index():
    with open("src/api/templates/interface.html", "r") as f:
        return HTMLResponse(content=f.read())
    
@router.get('/get_order_and_product_id')
async def get_order_and_product_id(session: SessionDep):
    try:
        orders = await session.execute(select(Order.id))
        products = await session.execute(select(Product.id))

        result_order = [{'id_ord': order_id} for order_id in orders.scalars()]
        result_prod = [{'id_prod': prod_id} for prod_id in products.scalars()]

        return result_order, result_prod

    except Exception as e:
        print(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail='Не удалось выполнить чтение из БД'
        )

@router.get("/orders/{order_id}/items", response_model=List[OrderItemResponse])
async def get_order_items(order_id: UUID, session: SessionDep):
    
    query = select(OrderItem).where(OrderItem.order_id == order_id).options(joinedload(OrderItem.product))
    result = await session.execute(query)
    order_items = result.scalars().all()
    
    return [
        OrderItemResponse(
            order_id=item.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=item.price_at_order,
            product_name=item.product.name
        ) for item in order_items
    ]