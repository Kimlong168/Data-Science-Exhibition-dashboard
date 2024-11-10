# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up page configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    product_df = pd.read_excel('data/Product.xlsx')
    sales_df = pd.read_excel('data/SalesData.xlsx')
    return product_df, sales_df

product_df, sales_df = load_data()

# Merge Data
merged_df = pd.merge(sales_df, product_df, left_on='ProductKey', right_on='ID')
merged_df['SalesAmount'] = merged_df['Quantity'] * merged_df['UnitPrice']


# Set seaborn style
sns.set(style="darkgrid")

# 1. Calculate Sales Amount
merged_df['SalesAmount'] = merged_df['Quantity'] * merged_df['UnitPrice']
st.write(merged_df)

#2 Display Total Revenue, Total Orders, and Average Order Value
total_revenue = merged_df['SalesAmount'].sum()
total_orders = merged_df['OrderNumber'].nunique()
average_order_value = total_revenue / total_orders

st.write(f"### Total Revenue: ${total_revenue}")
st.write(f"### Total Orders: {total_orders}")
st.write(f"### Average Order Value: ${average_order_value}")

# 3.1 Revenue by Channel (Bar and Pie charts)
st.subheader("Revenue by Sales Channel")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Channel', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Sales Channel")
ax.set_ylabel("Total Revenue")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 8))
channel_revenue = merged_df.groupby('Channel')['SalesAmount'].sum()
ax.pie(channel_revenue, labels=channel_revenue.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
ax.set_title("Revenue by Sales Channel")
st.pyplot(fig)

# 3.2 Revenue by Product Category (Bar and Pie charts)
st.subheader("Revenue by Product Category")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='ProductCategory', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Product Category")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 8))
category_revenue = merged_df.groupby('ProductCategory')['SalesAmount'].sum()
ax.pie(category_revenue, labels=category_revenue.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
ax.set_title("Revenue by Product Category")
st.pyplot(fig)

# 3.3 Revenue by Product Group (Bar and Pie charts)
st.subheader("Revenue by Product Group")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='ProductGroup', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Product Group")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 8))
product_group_revenue = merged_df.groupby('ProductGroup')['SalesAmount'].sum()
ax.pie(product_group_revenue, labels=product_group_revenue.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
ax.set_title("Revenue by Product Group")
st.pyplot(fig)

# 4.1 Orders by Product Category (Bar and Pie charts)
st.subheader("Orders by Product Category")

fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=merged_df, x='ProductCategory', ax=ax)
ax.set_title("Orders by Product Category")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 8))
category_orders = merged_df['ProductCategory'].value_counts()
ax.pie(category_orders, labels=category_orders.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
ax.set_title("Orders by Product Category")
st.pyplot(fig)

# 4.2 Orders by Salesperson (Bar and Pie charts)
st.subheader("Orders by Salesperson")

fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=merged_df, x='Salesperson', ax=ax)
ax.set_title("Orders by Salesperson")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(8, 8))
salesperson_orders = merged_df['Salesperson'].value_counts()
ax.pie(salesperson_orders, labels=salesperson_orders.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
ax.set_title("Orders by Salesperson")
st.pyplot(fig)

# 5. Revenue per Quarter and Month
st.subheader("Revenue by Quarter and Month")
merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'])
merged_df['Quarter'] = merged_df['OrderDate'].dt.to_period("Q")
merged_df['Month'] = merged_df['OrderDate'].dt.to_period("M")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Quarter', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Quarter")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Month', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Month")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# 6. Salesperson Performance
st.subheader("Salesperson Performance")
salesperson_summary = merged_df.groupby('Salesperson').agg({
    'SalesAmount': ['sum', 'mean'],
    'OrderNumber': 'nunique'
}).reset_index()
salesperson_summary.columns = ['Salesperson', 'TotalRevenue', 'AverageOrderValue', 'TotalOrders']

# Display salesperson summary table
st.write(salesperson_summary)

# Top Salesperson by Revenue
top_salesperson = salesperson_summary.loc[salesperson_summary['TotalRevenue'].idxmax()]
st.write(f"### Top Salesperson by Revenue: {top_salesperson['Salesperson']}, Revenue: ${top_salesperson['TotalRevenue']}")
