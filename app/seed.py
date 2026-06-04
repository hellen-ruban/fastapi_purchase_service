import asyncio

from sqlalchemy import delete

from app.database import async_session
from app.models import Product

async def seed_products():
    async with async_session() as session:
        await session.execute(delete(Product))

        products = [
            Product(stock=10, description="Magic Wand"),
            Product(stock=5, description="Magic Cauldron"),
            Product(stock=20, description="Healing Potion"),
            Product(stock=3, description="Phoenix Feather"),
            Product(stock=7, description="Invisibility Cloak"),
        ]

        session.add_all(products)

        await session.commit()

        print("Products seeded successfully")

async def main():
    await seed_products()

if __name__ == "__main__":
    asyncio.run(main())