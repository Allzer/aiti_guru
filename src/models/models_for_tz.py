from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Numeric, ForeignKey, DateTime, Enum
)

import enum

from database import Base

from sqlalchemy.orm import relationship

class OrderStatus(str, enum.Enum):
    new = "new"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    sku = Column(String, unique=True, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(12,2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.new, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Numeric(12,2), nullable=False)

    product = relationship("Product")
    order = relationship("Order")
