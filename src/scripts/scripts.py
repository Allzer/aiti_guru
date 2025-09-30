import asyncio
from datetime import datetime, timedelta
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


async def add_client() -> OrderItem:
    async with async_session_maker() as session:
        # --- client ---
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
            id=order_id,
            client_id=client_id,
            status=status,
            created_at=dg.gen_order_created_at(),
        )
        session.add(order)
        await session.commit()

        category_and_product = dg.gen_product_name()
        if isinstance(category_and_product, dict):
            category_and_product = list(category_and_product.items())

        all_product_ids = []
        product_price_map = {}

        for top_category_name, subcat_dicts in category_and_product:
            top_cat_id = dg.gen_uuid()
            top_cat = Category(id=top_cat_id, name=top_category_name, parent_id=None)
            session.add(top_cat)
            await session.commit()

            for subcat_dict in subcat_dicts:
                for subcat_name, sku_list in subcat_dict.items():
                    subcat_id = dg.gen_uuid()
                    subcat = Category(id=subcat_id, name=subcat_name, parent_id=top_cat_id)
                    session.add(subcat)
                    await session.commit()

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
                        await session.commit()

                        all_product_ids.append(product_id)
                        product_price_map[product_id] = price

        if not all_product_ids:
            return None

        created_order_item = None
        num_items = random.randint(1, 3)
        chosen = random.sample(all_product_ids, k=min(num_items, len(all_product_ids)))
        for pid in chosen:
            qty = random.randint(1, 5)
            price_at_order = product_price_map[pid]
            order_item = OrderItem(
                order_id=order_id,
                product_id=pid,
                quantity=qty,
                price_at_order=price_at_order,
            )
            session.add(order_item)
            await session.commit()
            await session.refresh(order_item)
            created_order_item = order_item

        return created_order_item


if __name__ == "__main__":
    created = asyncio.run(add_client())
    print('Данные добавлены')
