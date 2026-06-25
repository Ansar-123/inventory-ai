from database.db import SessionLocal
from database.models import Product

db = SessionLocal()

products = db.query(Product).all()

for product in products:
    print(
        product.id,
        product.name,
        product.category,
        product.price
    )