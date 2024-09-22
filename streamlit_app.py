import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title for the Streamlit app
st.title("E-commerce Order Analysis Dashboard")

def load_data():
    # Load the CSV files
    order_items = pd.read_csv('main_data/order_items_dataset.csv')
    orders = pd.read_csv('main_data/orders_dataset.csv')
    geolocation = pd.read_csv('main_data/geolocation_dataset.csv')

    # Data wrangling
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
    orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

    orders_cleaned = orders.dropna(subset=['order_delivered_customer_date', 'order_approved_at'])
    order_items_cleaned = order_items.dropna()

    merged_data = pd.merge(order_items_cleaned, orders_cleaned, on='order_id')

    # Create new features
    merged_data['estimated_delivery_time'] = (merged_data['order_estimated_delivery_date'] - merged_data['order_purchase_timestamp']).dt.days
    merged_data['approval_time'] = (merged_data['order_approved_at'] - merged_data['order_purchase_timestamp']).dt.total_seconds() / 3600
    merged_data['total_price'] = merged_data['price'] + merged_data['freight_value']
    merged_data['actual_delivery_time'] = (merged_data['order_delivered_customer_date'] - merged_data['order_purchase_timestamp']).dt.days

    return merged_data, order_items, orders, geolocation

# Load data
data, order_items, orders, geolocation = load_data()

# Load the logo and center it
st.sidebar.image('logo_sim.png', width=150)

# Dashboard name below the logo
st.sidebar.write("Dashboard Analytics by Annisa Shafa")

# Sidebar for navigation
st.sidebar.title("Navigation Menu")
page = st.sidebar.selectbox("Choose a page", ('Home', 'Analysis', 'Dataset', 'About Me'))

# Home Page
if page == 'Home':
    st.header("Welcome to the Dashboard!")

# Analysis Submenu
elif page == 'Analysis':
    analysis = st.sidebar.selectbox("Choose an analysis", ('Delivery Estimation', 'Freight Value', 'Price & Delivery Correlation'))

    if analysis == 'Delivery Estimation':
        st.header("Delivery Estimation Analysis")

        # Histogram: Estimated Delivery Time
        st.subheader("Estimated Delivery Time Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(data['estimated_delivery_time'], bins=30, kde=True, color='blue')
        plt.title("Distribution of Estimated Delivery Time (Days)")
        plt.xlabel("Days")
        plt.ylabel("Frequency")
        st.pyplot(plt)

        # Heatmap: Correlation between factors affecting delivery time
        st.subheader("Correlation Between Factors and Delivery Time")
        corr = data[['price', 'freight_value', 'approval_time', 'estimated_delivery_time']].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("Correlation Between Factors and Delivery Time")
        st.pyplot(plt)

    elif analysis == 'Freight Value':
        st.header("Freight Value Contribution Analysis")

        # Scatter plot: Freight Value vs Total Price
        st.subheader("Freight Value vs Total Order Price")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='freight_value', y='total_price', data=data, color='green')
        plt.title("Freight Value vs Total Price")
        plt.xlabel("Freight Value")
        plt.ylabel("Total Price")
        st.pyplot(plt)

        # Correlation: Freight Value and Total Price
        st.subheader("Correlation Between Freight Value and Total Price")
        corr_freight = data[['freight_value', 'total_price']].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_freight, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("Correlation Between Freight Value and Total Price")
        st.pyplot(plt)

    elif analysis == 'Price & Delivery Correlation':
        st.header("Price and Delivery Time Correlation")
        
        # Scatter plot: Price vs Actual Delivery Time
        st.subheader("Product Price vs Actual Delivery Time")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='price', y='actual_delivery_time', data=data, color='purple')
        plt.title("Price vs Actual Delivery Time")
        plt.xlabel("Price")
        plt.ylabel("Actual Delivery Time (Days)")
        st.pyplot(plt)

        # Correlation Heatmap: Price and Delivery Time
        st.subheader("Correlation Between Price and Delivery Time")
        corr_price_delivery = data[['price', 'actual_delivery_time']].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_price_delivery, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title("Correlation Between Price and Delivery Time")
        st.pyplot(plt)

# Dataset Submenu
elif page == 'Dataset':
    dataset = st.sidebar.selectbox("Choose a dataset to view", ('Order Items', 'Orders', 'Geolocation'))

    if dataset == 'Order Items':
        st.header("Order Items Dataset")
        st.dataframe(order_items)
        st.download_button("Download Order Items Dataset", order_items.to_csv(index=False).encode('utf-8'), "order_items_dataset.csv", "text/csv")

    elif dataset == 'Orders':
        st.header("Orders Dataset")
        st.dataframe(orders)
        st.download_button("Download Orders Dataset", orders.to_csv(index=False).encode('utf-8'), "orders_dataset.csv", "text/csv")

    elif dataset == 'Geolocation':
        st.header("Geolocation Dataset")
        st.dataframe(geolocation)
        st.download_button("Download Geolocation Dataset", geolocation.to_csv(index=False).encode('utf-8'), "geolocation_dataset.csv", "text/csv")

# About Me Page
elif page == 'About Me':
    st.header("About Me")
    st.write("Annisa Shafa Brilianty Lebeharia")
    st.write("M284B4KX0584 | ML-15")
