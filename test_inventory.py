from services.inventory_service import (
    add_product,
    add_stock,
    record_sale
)

# Create Product
add_product(
    name="Laptop",
    category="Electronics",
    price=50000,
    reorder_level=10
)

# Add Initial Stock
add_stock(
    product_id=1,
    quantity=50,
    note="Initial Stock"
)

# Record Sale
record_sale(
    product_id=1,
    quantity=5
)