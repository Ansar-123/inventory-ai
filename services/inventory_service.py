from database.db import SessionLocal
from database.models import (
    Product,
    Inventory,
    InventoryTransaction,
    Sale
)

db = SessionLocal()


def add_product(
    name,
    category,
    price,
    reorder_level
):
    product = Product(
        name=name,
        category=category,
        price=price,
        reorder_level=reorder_level
    )

    db.add(product)
    db.commit()

    print("Product added successfully")


def add_stock(
    product_id,
    quantity,
    note="Stock Added"
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if inventory:
        inventory.quantity += quantity

    else:
        inventory = Inventory(
            product_id=product_id,
            quantity=quantity
        )

        db.add(inventory)

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type="IN",
        quantity=quantity,
        note=note
    )

    db.add(transaction)
    db.commit()

    print("Stock added successfully")


def record_sale(
    product_id,
    quantity
):
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()

    if not inventory:
        print("Inventory not found")
        return

    if inventory.quantity < quantity:
        print("Insufficient stock")
        return

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    inventory.quantity -= quantity

    sale = Sale(
        product_id=product_id,
        quantity=quantity,
        unit_price=product.price,
        total_amount=product.price * quantity
    )

    transaction = InventoryTransaction(
        product_id=product_id,
        transaction_type="OUT",
        quantity=quantity,
        note="Sale"
    )

    db.add(sale)
    db.add(transaction)

    db.commit()

    print("Sale recorded successfully")