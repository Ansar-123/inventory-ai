import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
import streamlit as st
import pandas as pd

from database.db import SessionLocal
from database.models import Product, Inventory

st.title("AI Inventory Management System")

db = SessionLocal()
st.subheader("Add New Product")

with st.form("product_form"):

    product_name = st.text_input("Product Name")

    category = st.text_input("Category")

    price = st.number_input(
        "Price",
        min_value=0.0
    )

    reorder_level = st.number_input(
        "Reorder Level",
        min_value=0
    )

    submit_button = st.form_submit_button(
        "Add Product"
    )

    if submit_button:

        new_product = Product(
            name=product_name,
            category=category,
            price=price,
            reorder_level=reorder_level
        )

        db.add(new_product)

        db.commit()

        st.success(
            "Product Added Successfully!"
        )
products = db.query(Product).all()
inventory = db.query(Inventory).all()
from database.models import Sale

sales = db.query(Sale).all()

total_revenue = sum(
    sale.total_amount
    for sale in sales
)

st.subheader("Project Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Products", len(products))

total_stock = sum(item.quantity for item in inventory)

col2.metric("Total Stock", total_stock)
col3.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

st.subheader("Products")

product_data = []

for product in products:
    product_data.append({
        "ID": product.id,
        "Name": product.name,
        "Category": product.category,
        "Price": product.price,
        "Reorder Level": product.reorder_level
    })

df = pd.DataFrame(product_data)

st.dataframe(df)
st.subheader("Low Stock Alerts")

low_stock_products = []

for product in products:

    inventory_item = db.query(Inventory).filter(
        Inventory.product_id == product.id
    ).first()

    if inventory_item and inventory_item.quantity <= product.reorder_level:

        low_stock_products.append({
            "Product": product.name,
            "Current Stock": inventory_item.quantity,
            "Reorder Level": product.reorder_level
        })

if low_stock_products:
    st.warning("Low Stock Products Found!")

    low_stock_df = pd.DataFrame(low_stock_products)

    st.dataframe(low_stock_df)

else:
    st.success("No Low Stock Products")

st.subheader("Inventory Overview")

inventory_data = []

for product in products:

    inventory_item = db.query(Inventory).filter(
        Inventory.product_id == product.id
    ).first()

    current_stock = (
        inventory_item.quantity
        if inventory_item
        else 0
    )

    status = (
        "Low Stock"
        if current_stock <= product.reorder_level
        else "Normal"
    )

    inventory_data.append({
        "Product": product.name,
        "Current Stock": current_stock,
        "Reorder Level": product.reorder_level,
        "Status": status
    })

inventory_df = pd.DataFrame(inventory_data)

st.dataframe(inventory_df)