import asyncio

from sqlalchemy import select

from app.database import async_session
from app.models import Product


async def show_products():
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        for product in products:
            print(
                product.product_id,
                product.description,
                product.stock
            )


async def main():
    await show_products()


if __name__ == "__main__":
    asyncio.run(main())