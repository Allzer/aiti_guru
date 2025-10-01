import asyncio
from pathlib import Path
import random
import sys

from sqlalchemy import select

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from database import async_session_maker
import src.scripts.datagen as dg
from src.models.models_for_tz import (
    Client,
    Category,
    Product,
    Order,
    OrderItem,
    OrderStatus,
)

async def ensure_categories_and_products_exist():
    """
    Создает категории и продукты, если они еще не существуют.
    Возвращает словарь {product_id: price} для использования при создании заказов.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(Product))
        existing_products = result.scalars().all()
        
        if existing_products:
            return {product.id: product.price for product in existing_products}
        
        product_price_map = {}
        category_and_product = dg.gen_product_name()
        
        if isinstance(category_and_product, dict):
            category_and_product = list(category_and_product.items())

        for top_category_name, subcat_dicts in category_and_product:
            top_cat_id = dg.gen_uuid()
            top_cat = Category(id=top_cat_id, name=top_category_name, parent_id=None)
            session.add(top_cat)

            for subcat_dict in subcat_dicts:
                for subcat_name, sku_list in subcat_dict.items():
                    subcat_id = dg.gen_uuid()
                    subcat = Category(id=subcat_id, name=subcat_name, parent_id=top_cat_id)
                    session.add(subcat)

                    for sku in sku_list:
                        product_id = dg.gen_uuid()
                        price = dg.gen_price()
                        product = Product(
                            id=product_id,
                            name=sku,
                            category_id=subcat_id,
                            parent_id=top_cat_id,
                            stock_quantity=random.randint(0, 30),
                            price=price,
                        )
                        session.add(product)
                        product_price_map[product_id] = price

        await session.commit()
        return product_price_map

async def add_clients(num_clients=5):
    """
    Создает указанное количество клиентов с заказами.
    Использует существующие продукты для позиций заказа.
    """
    product_price_map = await ensure_categories_and_products_exist()
    product_ids = list(product_price_map.keys())

    async with async_session_maker() as session:
        for _ in range(num_clients):
            name = dg.gen_people()
            client_id = dg.gen_uuid()
            client = Client(
                id=client_id,
                name=name,
                email=dg.gen_random_email(),
                address=dg.gen_address(),
            )
            session.add(client)

            status = random.choice([
                OrderStatus.new,
                OrderStatus.processing,
                OrderStatus.completed,
                OrderStatus.cancelled,
            ])
            order_id = dg.gen_uuid()
            order = Order(
                id=order_id,
                client_id=client_id,
                status=status,
                created_at=dg.gen_order_created_at(),
            )
            session.add(order)

            num_items = random.randint(1, min(3, len(product_ids)))
            chosen_products = random.sample(product_ids, k=num_items)
            
            for product_id in chosen_products:
                qty = random.randint(1, 5)
                price_at_order = product_price_map[product_id]
                order_item = OrderItem(
                    order_id=order_id,
                    product_id=product_id,
                    quantity=qty,
                    price_at_order=price_at_order,
                )
                session.add(order_item)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_clients(10))
    print('Данные добавлены')