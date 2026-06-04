from fastapi import FastAPI, HTTPException
from sqlalchemy import select

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
        result = await session.execute(
            select(Product).where(Product.product_id == request.product_id)
        )

        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        if product.stock < request.purchased_count:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )
        product.stock -= request.purchased_count

        await session.commit()

        return {
            "message": "Purchase successful",
            "product": product.description,
            "remaining_stock": product.stock,
        }

