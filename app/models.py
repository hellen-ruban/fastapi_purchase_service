from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    stock: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)