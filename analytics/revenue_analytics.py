import pandas as pd
from database.models import Product, Sale


def get_revenue_by_product(db):

    sales = db.query(Sale).all()

    revenue_data = []

    for sale in sales:

        product = db.query(Product).filter(
            Product.id == sale.product_id
        ).first()

        revenue_data.append({
            "Product": product.name,
            "Revenue": sale.total_amount
        })

    revenue_df = pd.DataFrame(revenue_data)

    if revenue_df.empty:
        return revenue_df

    revenue_df = revenue_df.groupby(
        "Product",
        as_index=False
    )["Revenue"].sum()

    return revenue_df