from database.db import SessionLocal
from database.models import Product

db = SessionLocal()

product = db.query(Product).filter(Product.name == "Mouse").first()

if product:
    product.price = 700
    db.commit()
    print("Price updated successfully!")
else:
    print("Product not found")