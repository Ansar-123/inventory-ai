import pandas as pd

from database.models import (
    Product,
    Inventory
)


def get_inventory_value(db):

    products = db.query(Product).all()

    inventory_value = []

    total_inventory_value = 0

    for product in products:

        inventory = db.query(Inventory).filter(
            Inventory.product_id == product.id
        ).first()

        quantity = inventory.quantity if inventory else 0

        value = quantity * product.price

        total_inventory_value += value

        inventory_value.append({
            "Product": product.name,
            "Stock": quantity,
            "Price": product.price,
            "Inventory Value": value
        })

    inventory_df = pd.DataFrame(inventory_value)

    return inventory_df, total_inventory_value