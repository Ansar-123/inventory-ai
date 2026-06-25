from database.db import SessionLocal
from database.models import Product

db = SessionLocal()

product = db.query(Product).filter(Product.name == "SSD").first()

if product:
    db.delete(product)
    db.commit()
    print("Product deleted successfully!")
else:
    print("Product not found")