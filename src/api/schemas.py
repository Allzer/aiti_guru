from uuid import UUID
from pydantic import BaseModel, PositiveInt
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int = 0

class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    client_id: Optional[int] = None

class OrderOut(BaseModel):
    id: int
    client_id: Optional[int]
    status: str

    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: PositiveInt

class OrderItemResponse(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: int
    price_at_order: float
    product_name: str

class AddItemResponse(OrderItemResponse):
    created: bool