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

class OrderItemOut(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_order: float
    product_name: Optional[str] = None

    class Config:
        orm_mode = True