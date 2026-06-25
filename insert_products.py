from database.db import SessionLocal
from database.models import Product

db = SessionLocal()

products = [
    Product(name="Laptop", category="Electronics", price=50000),
    Product(name="Mouse", category="Electronics", price=500),
    Product(name="Keyboard", category="Electronics", price=1200),
    Product(name="SSD", category="Electronics", price=800),
    Product(name="Monitor", category="Electronics", price=6000)
]

db.add_all(products)
db.commit()

print("Products inserted successfully!")