from fastapi import FastAPI
from database.db import SessionLocal
from database.models import Product
from api.schemas import (
    ProductCreate,
    ProductUpdate
)
app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Welcome to AI Inventory Management API"
    }
@app.get("/products")
def get_products():

    db = SessionLocal()

    products = db.query(Product).all()

    product_list = []

    for product in products:

        product_list.append({
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "reorder_level": product.reorder_level
        })

    db.close()

    return product_list
@app.post("/products")
def create_product(product: ProductCreate):

    db = SessionLocal()

    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        reorder_level=product.reorder_level
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    db.close()

    return {
        "message": "Product created successfully",
        "product_id": new_product.id
    }
@app.put("/products/{product_id}")
def update_product_api(
    product_id: int,
    product: ProductUpdate
):

    db = SessionLocal()

    existing_product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing_product:
        db.close()
        return {
            "message": "Product not found"
        }

    existing_product.name = product.name
    existing_product.category = product.category
    existing_product.price = product.price
    existing_product.reorder_level = product.reorder_level

    db.commit()
    db.refresh(existing_product)

    db.close()

    return {
        "message": "Product updated successfully"
    }
@app.delete("/products/{product_id}")
def delete_product_api(product_id: int):

    db = SessionLocal()

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        db.close()
        return {
            "message": "Product not found"
        }

    db.delete(product)
    db.commit()

    db.close()

    return {
        "message": "Product deleted successfully"
    }