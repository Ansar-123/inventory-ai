import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)
import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import SessionLocal
from database.models import Product, Inventory
from services.inventory_service import (
    add_stock,
    record_sale,
    update_product,
    delete_product
)
from client.api_client import get_products
from analytics.revenue_analytics import get_revenue_by_product
from analytics.inventory_analytics import get_inventory_value

st.title("AI Inventory Management System")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Inventory",
    "Sales",
    "Management"
])
db = SessionLocal()
products = get_products()

product_dict = {
    product["name"]: product["id"]
    for product in products
}
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



st.subheader("Add Stock")

with st.form("stock_form"):

    selected_product = st.selectbox(
        "Select Product",
        list(product_dict.keys()),
        key="stock_product"
    )

    product_id = product_dict[selected_product]

    stock_quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    note = st.text_input(
        "Note",
        placeholder="Example: Purchased from Dell"
    )

    stock_submit = st.form_submit_button(
        "Add Stock"
    )

    if stock_submit:

        add_stock(
            product_id,
            stock_quantity,
            note
        )

        st.success("Stock Added Successfully!")

#  RECORD SALE 

st.subheader("Record Sale")

with st.form("sale_form"):

    selected_sale_product = st.selectbox(
        "Select Product",
        list(product_dict.keys()),
        key="sale_product"
    )

    sale_product_id = product_dict[selected_sale_product]

    sale_quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1,
        key="sale_quantity"
    )

    sale_submit = st.form_submit_button(
        "Record Sale"
    )

    if sale_submit:

     record_sale(
        sale_product_id,
        sale_quantity
    )

    st.success("Sale Recorded Successfully!")
# ---------- EDIT PRODUCT ----------

st.subheader("Edit Product")

with st.form("edit_product_form"):

    selected_product = st.selectbox(
        "Select Product",
        list(product_dict.keys()),
        key="edit_product"
    )

    edit_product_id = product_dict[selected_product]

    product = db.query(Product).filter(
        Product.id == edit_product_id
    ).first()

    new_name = st.text_input(
        "Product Name",
        value=product.name
    )

    new_category = st.text_input(
        "Category",
        value=product.category
    )

    new_price = st.number_input(
        "Price",
        value=float(product.price)
    )

    new_reorder_level = st.number_input(
        "Reorder Level",
        value=product.reorder_level
    )

    update_submit = st.form_submit_button(
        "Update Product"
    )

    if update_submit:

        update_product(
            edit_product_id,
            new_name,
            new_category,
            new_price,
            new_reorder_level
        )

        st.success("Product Updated Successfully!")

#DELETE PRODUCT

st.subheader("Delete Product")

with st.form("delete_product_form"):

    selected_delete_product = st.selectbox(
        "Select Product",
        list(product_dict.keys()),
        key="delete_product"
    )

    delete_product_id = product_dict[selected_delete_product]

    delete_submit = st.form_submit_button(
        "Delete Product"
    )

    if delete_submit:

        result = delete_product(delete_product_id)

        if result:
            st.success("Product Deleted Successfully!")

        else:
            st.error(
                "Cannot delete product because it has inventory, sales, or transaction records."
            )

inventory = db.query(Inventory).all()
from database.models import Sale

sales = db.query(Sale).all()
sales_data = []

for sale in sales:

    product = db.query(Product).filter(
        Product.id == sale.product_id
    ).first()

    sales_data.append({
        "Product": product.name,
        "Quantity Sold": sale.quantity,
        "Revenue": sale.total_amount
    })

sales_df = pd.DataFrame(sales_data)

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

search_text = st.text_input(
    "Search Product",
    placeholder="Enter product name..."
)
product_data = []

for product in products:
    product_data.append({
        "ID": product["id"],
        "Name": product["name"],
        "Category": product["category"],
        "Price": product["price"],
        "Reorder Level": product["reorder_level"]
    })

df = pd.DataFrame(product_data)

if search_text:

    df = df[
        df["Name"].str.contains(
            search_text,
            case=False
        )
    ]


st.dataframe(df)
st.subheader("Low Stock Alerts")

low_stock_products = []

for product in products:

    inventory_item = db.query(Inventory).filter(
        Inventory.product_id == product["id"]
    ).first()

    if inventory_item and inventory_item.quantity <= product["reorder_level"]:

        low_stock_products.append({
            "Product": product["name"],
            "Current Stock": inventory_item.quantity,
            "Reorder Level": product["reorder_level"]
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
        Inventory.product_id == product["id"]
    ).first()

    current_stock = (
        inventory_item.quantity
        if inventory_item
        else 0
    )

    status = (
        "Low Stock"
        if current_stock <= product["reorder_level"]
        else "Normal"
    )

    inventory_data.append({
        "Product": product["name"],
        "Current Stock": current_stock,
        "Reorder Level": product["reorder_level"],
        "Status": status
    })

inventory_df = pd.DataFrame(inventory_data)

st.dataframe(inventory_df)
st.subheader("Inventory Distribution")

fig = px.bar(
    inventory_df,
    x="Product",
    y="Current Stock",
    color="Status",
    text="Current Stock",
    title="Current Inventory by Product",
    color_discrete_map={
        "Normal": "green",
        "Low Stock": "red"
    }
)

fig.update_traces(textposition="outside")

fig.update_layout(
    xaxis_title="Product",
    yaxis_title="Stock Quantity",
    title_x=0.3,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Product Stock Distribution")

pie_chart = px.pie(
    inventory_df,
    names="Product",
    values="Current Stock",
    title="Stock Percentage by Product",
    hole=0.4
)

st.plotly_chart(
    pie_chart,
    use_container_width=True
)
st.subheader("Best Selling Products")

if not sales_df.empty:

    best_sales = sales_df.groupby(
        "Product",
        as_index=False
    )["Quantity Sold"].sum()

    sales_chart = px.bar(
        best_sales,
        x="Product",
        y="Quantity Sold",
        text="Quantity Sold",
        color="Quantity Sold",
        title="Best Selling Products"
    )

    sales_chart.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        sales_chart,
        use_container_width=True
    )

else:

    st.info("No sales data available.")

st.subheader("Revenue by Product")

revenue_df = get_revenue_by_product(db)

if not revenue_df.empty:

    revenue_chart = px.bar(
        revenue_df,
        x="Product",
        y="Revenue",
        text="Revenue",
        color="Revenue",
        title="Revenue by Product"
    )

    revenue_chart.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        revenue_chart,
        use_container_width=True
    )

else:

    st.info("No revenue data available.")

st.subheader("Inventory Value Analysis")

inventory_value_df, total_inventory_value = get_inventory_value(db)

st.metric(
    "Total Inventory Value",
    f"₹{total_inventory_value:,.2f}"
)

st.dataframe(inventory_value_df)

inventory_value_chart = px.bar(
    inventory_value_df,
    x="Product",
    y="Inventory Value",
    text="Inventory Value",
    color="Inventory Value",
    title="Inventory Value by Product"
)

inventory_value_chart.update_traces(
    textposition="outside"
)

inventory_value_chart.update_layout(
    xaxis_title="Product",
    yaxis_title="Inventory Value (₹)",
    title_x=0.25,
    height=500
)

st.plotly_chart(
    inventory_value_chart,
    use_container_width=True
)