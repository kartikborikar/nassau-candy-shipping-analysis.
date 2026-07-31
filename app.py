import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Nassau Candy Shipping Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Factory-to-Customer Shipping Route Efficiency Analysis")
st.write("Nassau Candy Distributor Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

    df["Delivery Days"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    return df

df = load_data()

st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique())
)

ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    ["All"] + sorted(df["Ship Mode"].unique())
)

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if ship_mode != "All":
    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == ship_mode
    ]

st.header("Dataset Preview")
st.dataframe(filtered_df.head())

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${filtered_df['Sales'].sum():,.2f}"
)

col2.metric(
    "Orders",
    filtered_df["Order ID"].nunique()
)

col3.metric(
    "Gross Profit",
    f"${filtered_df['Gross Profit'].sum():,.2f}"
)

col4.metric(
    "Avg Delivery Days",
    round(filtered_df["Delivery Days"].mean(), 2)
)



Part 2: Charts & Analysis

# ---------------------------------------
# Sales by Region
# ---------------------------------------

st.header("📊 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8,5))
region_sales.plot(kind="bar", ax=ax)
ax.set_title("Sales by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Sales")
plt.xticks(rotation=45)

st.pyplot(fig)

# ---------------------------------------
# Gross Profit by Region
# ---------------------------------------

st.header("💰 Gross Profit by Region")

profit_region = filtered_df.groupby("Region")["Gross Profit"].sum()

fig, ax = plt.subplots(figsize=(8,5))
profit_region.plot(kind="bar", ax=ax)

ax.set_title("Gross Profit by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Gross Profit")

plt.xticks(rotation=45)

st.pyplot(fig)

# ---------------------------------------
# Sales by Ship Mode
# ---------------------------------------

st.header("🚚 Sales by Ship Mode")

ship_sales = filtered_df.groupby("Ship Mode")["Sales"].sum()

fig, ax = plt.subplots(figsize=(7,5))
ship_sales.plot(kind="bar", ax=ax)

ax.set_title("Sales by Ship Mode")
ax.set_xlabel("Ship Mode")
ax.set_ylabel("Sales")

plt.xticks(rotation=45)

st.pyplot(fig)

# ---------------------------------------
# Monthly Sales Trend
# ---------------------------------------

filtered_df["Month"] = filtered_df["Order Date"].dt.month_name()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reindex(month_order)
)

st.header("📅 Monthly Sales Trend")

fig, ax = plt.subplots(figsize=(10,5))

monthly_sales.plot(
    kind="line",
    marker="o",
    linewidth=3,
    ax=ax
)

ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")

plt.xticks(rotation=45)

st.pyplot(fig)

Part 3: Top Products, Customers, States & Cities

# ---------------------------------------
# Top 10 Products
# ---------------------------------------

st.header("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)

fig, ax = plt.subplots(figsize=(10,5))
top_products.sort_values().plot(kind="barh", ax=ax)
ax.set_title("Top 10 Products by Sales")
ax.set_xlabel("Sales")
st.pyplot(fig)

# ---------------------------------------
# Top 10 Customers
# ---------------------------------------

st.header("👥 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer ID")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_customers)

# ---------------------------------------
# Top 10 States
# ---------------------------------------

st.header("📍 Top 10 States")

top_states = (
    filtered_df.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
top_states.sort_values().plot(kind="barh", ax=ax)
ax.set_title("Top 10 States by Sales")
ax.set_xlabel("Sales")
st.pyplot(fig)

# ---------------------------------------
# Top 10 Cities
# ---------------------------------------

st.header("🏙️ Top 10 Cities")

top_cities = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
top_cities.sort_values().plot(kind="barh", ax=ax)
ax.set_title("Top 10 Cities by Sales")
ax.set_xlabel("Sales")
st.pyplot(fig)

Part 4: Business Insights

# ---------------------------------------
# Business Insights
# ---------------------------------------

st.header("💡 Business Insights")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
avg_delivery = filtered_df["Delivery Days"].mean()

highest_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

highest_shipmode = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .idxmax()
)

st.success(f"""
✅ Total Sales: ${total_sales:,.2f}

✅ Total Gross Profit: ${total_profit:,.2f}

✅ Average Delivery Days: {avg_delivery:.2f} Days

✅ Best Performing Region: {highest_region}

✅ Best Performing Ship Mode: {highest_shipmode}
""")

# ---------------------------------------
# Dataset Summary
# ---------------------------------------

st.header("📋 Dataset Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Orders",
        "Total Products",
        "Total Customers",
        "Total Regions"
    ],
    "Value": [
        len(filtered_df),
        filtered_df["Order ID"].nunique(),
        filtered_df["Product ID"].nunique(),
        filtered_df["Customer ID"].nunique(),
        filtered_df["Region"].nunique()
    ]
})

st.dataframe(summary)

# ---------------------------------------
# Conclusion
# ---------------------------------------

st.header("📌 Conclusion")

st.info("""
This dashboard analyzes shipping efficiency, sales performance,
customer behavior, and regional performance of Nassau Candy Distributor.

The analysis helps businesses identify high-performing regions,
optimize shipping methods, improve delivery performance,
and make better data-driven decisions.
""")

# ---------------------------------------
# Footer
# ---------------------------------------

st.markdown("---")

st.markdown(
    "### 👨‍💻 Developed by Kartik Dnyaneshwar Borikar"
)

st.caption("Data Analyst Fellowship Project | Unified Mentor")

