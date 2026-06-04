from fastapi import FastAPI, HTTPException
from sqlalchemy import select, update

from app.database import async_session
from app.models import Product
from app.schemas import PurchaseRequest

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Magic Shop API"}

@app.get("/products")
async def get_products():
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

        return [
            {
                "product_id": product.product_id,
                "description": product.description,
                "stock": product.stock,
            }
            for product in products
        ]

@app.post("/purchase")
async def purchase(request: PurchaseRequest):
    async with async_session() as session:
        statement = (
            update(Product)
            .where(Product.product_id == request.product_id)
            .where(Product.stock >= request.purchased_count)
            .values(stock=Product.stock - request.purchased_count)
            .returning(Product.product_id)
        )

        result = await session.execute(statement)
        updated_product_id = result.scalar_one_or_none()

        if updated_product_id is None:
            product_result = await session.execute(
                select(Product).where(Product.product_id == request.product_id)
            )
            product = product_result.scalar_one_or_none()

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

        await session.commit()

        return {"status": "success"}

