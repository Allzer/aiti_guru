import asyncio
from datetime import datetime
from pathlib import Path
import random
import sys

from sqlalchemy import select

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from database import async_session_maker
from src.models.models_for_tz import (
    Client,
    Category,
    Product,
    Order,
    OrderItem,
    OrderStatus,
)

# импортируем генераторы как dg
import src.scripts.datagen as dg


async def add_client() -> Client:
    async with async_session_maker() as session:
        name = dg.gen_people()

        client_id = dg.gen_uuid()
        client = Client(
            id=client_id,
            name=name,
            email=dg.gen_random_email(),
            address=dg.gen_address(),
        )
        session.add(client)
        await session.commit()
        
        status = random.choice([
            OrderStatus.new,
            OrderStatus.processing,
            OrderStatus.completed,
            OrderStatus.cancelled,
        ])

        order_id = dg.gen_uuid()
        order = Order(
            id = order_id,
            client_id=client_id,
            status=status,
        )
        session.add(order)
        await session.commit()

        category_and_product = dg.gen_product_name()
        for category_name, products in category_and_product:
            category_id = dg.gen_uuid()
            category = Category(
                id=category_id,
                name=category_name
            )
            session.add(category)
            await session.commit()

            list_product_id = []
            product_price = dg.gen_price()
            for product in products:
                product_id = dg.gen_uuid()
                producti = Product(
                    id=product_id,
                    name=product,
                    category_id=category_id,
                    stock_quantity=random.randint(0, 30),
                    price=product_price,
                )
                session.add(producti)
                await session.commit()
                list_product_id.append(product_id)
               
        quantity = random.randint(1, 5)
        order_item = OrderItem(
            order_id=order_id,
            product_id=random.choice(list_product_id),
            quantity=quantity,
            price_at_order=product_price,
        )
        session.add(order_item)
        await session.commit()
        await session.refresh(order_item)
        return order_item


async def add_all() -> None:

    await add_client()

    print('Данные добавлены')

    # # позиции заказа
    # for _ in range(records_per_entity * 3):
    #     await add_order_item()


if __name__ == "__main__":
    asyncio.run(add_all())
