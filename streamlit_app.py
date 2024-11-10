import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up page configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Load data
@st.cache
def load_data():
    product_df = pd.read_excel('data/Product.xlsx')
    sales_df = pd.read_excel('data/SalesData.xlsx')
    return product_df, sales_df

product_df, sales_df = load_data()

# Merge Data
merged_df = pd.merge(sales_df, product_df, left_on='ProductKey', right_on='ID')
merged_df['SalesAmount'] = merged_df['Quantity'] * merged_df['UnitPrice']

# Set seaborn style
sns.set(style="whitegrid")

# Dashboard title
st.title("Sales Dashboard")

# 1. Calculate the Sales Amount for each transaction
st.subheader("Sales Amount per Transaction")
st.write(merged_df[['OrderNumber', 'SalesAmount']])

# 2. Total revenue, total orders, and average order value
total_revenue = merged_df['SalesAmount'].sum()
total_orders = merged_df['OrderNumber'].nunique()
average_order_value = total_revenue / total_orders

st.subheader("Summary Statistics")
st.metric("Total Revenue", f"${total_revenue:,.2f}")
st.metric("Total Orders", total_orders)
st.metric("Average Order Value", f"${average_order_value:,.2f}")

# 3. Revenue by Channel
st.subheader("Revenue by Sales Channel")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Channel', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Sales Channel")
ax.set_ylabel("Total Revenue")
st.pyplot(fig)

# Revenue by Product Category
st.subheader("Revenue by Product Category")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='ProductCategory', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Product Category")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# Pie chart for Revenue by Product Category
st.subheader("Revenue Distribution by Product Category")
category_revenue = merged_df.groupby('ProductCategory')['SalesAmount'].sum()
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(category_revenue, labels=category_revenue.index, autopct='%1.1f%%', startangle=140)
ax.set_title("Revenue Distribution by Product Category")
st.pyplot(fig)

# Revenue by Product Group
st.subheader("Revenue by Product Group")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='ProductGroup', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Product Group")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# Revenue by Salesperson
st.subheader("Revenue by Salesperson")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Salesperson', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Salesperson")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# 4. Orders by Product Category
st.subheader("Number of Orders by Product Category")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=merged_df, x='ProductCategory', ax=ax)
ax.set_title("Number of Orders by Product Category")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# Orders by Salesperson
st.subheader("Number of Orders by Salesperson")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=merged_df, x='Salesperson', ax=ax)
ax.set_title("Number of Orders by Salesperson")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# 5. Revenue per Quarter and Month
merged_df['OrderDate'] = pd.to_datetime(merged_df['OrderDate'])
merged_df['Quarter'] = merged_df['OrderDate'].dt.to_period("Q")
merged_df['Month'] = merged_df['OrderDate'].dt.to_period("M")

# Revenue by Quarter
st.subheader("Revenue by Quarter")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Quarter', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Quarter")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# Revenue by Month
st.subheader("Revenue by Month")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=merged_df, x='Month', y='SalesAmount', estimator=sum, errorbar=None, ax=ax)
ax.set_title("Revenue by Month")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# 6. Salesperson Performance: Total Orders, Average Order Value, and Total Revenue
salesperson_summary = merged_df.groupby('Salesperson').agg({
    'SalesAmount': ['sum', 'mean'],
    'OrderNumber': 'nunique'
}).reset_index()
salesperson_summary.columns = ['Salesperson', 'TotalRevenue', 'AverageOrderValue', 'TotalOrders']

# Plot: Total Revenue by Salesperson
st.subheader("Total Revenue by Salesperson")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=salesperson_summary, x='Salesperson', y='TotalRevenue', errorbar=None, ax=ax)
ax.set_title("Total Revenue by Salesperson")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot: Average Order Value by Salesperson
st.subheader("Average Order Value by Salesperson")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=salesperson_summary, x='Salesperson', y='AverageOrderValue', errorbar=None, ax=ax)
ax.set_title("Average Order Value by Salesperson")
ax.set_ylabel("Average Order Value")
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot: Total Orders by Salesperson
st.subheader("Total Orders by Salesperson")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=salesperson_summary, x='Salesperson', y='TotalOrders', errorbar=None, ax=ax)
ax.set_title("Total Orders by Salesperson")
ax.set_ylabel("Total Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# Display top salesperson by revenue
top_salesperson = salesperson_summary.loc[salesperson_summary['TotalRevenue'].idxmax()]
st.subheader("Top Salesperson by Revenue")
st.write(f"Top Salesperson by Revenue: {top_salesperson['Salesperson']}, Revenue: ${top_salesperson['TotalRevenue']:,.2f}")
