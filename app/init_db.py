import asyncio

from app.database import reset_tables


async def main():
    await reset_tables()
    print("Tables reset successfully")


if __name__ == "__main__":
    asyncio.run(main())