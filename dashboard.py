import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=30000, limit=None, key="datarefresh")

# Connect Mongo
client = MongoClient("mongodb://127.0.0.1")
db = client["logistique"]
collection = db["stats"]

# Read latest statistics
stats = collection.find().sort("_id", -1).limit(1)[0]

# Remove _id for cleanliness
stats.pop("_id", None)

st.set_page_config(page_title="Dashboard Logistique", layout="wide")
st.title("📦 Dashboard Logistique - Analyse des prédictions")

# Distribution des prédictions
col1, col2 = st.columns(2)
col1.subheader("💰 Moyenne Order Item Total")
col1.metric("", f"{stats['avg_order_item_total']:.2f}")
df_pred = pd.DataFrame(stats["prediction_distribution"])
col2.subheader("📈 Distribution des prédictions")
col2.bar_chart(df_pred.set_index("prediction"))
st.divider()

# Count by category
st.subheader("📊 Nombre de commandes par catégorie")
df_cat = pd.DataFrame(stats["count_by_category"])
df_cat["count"] = pd.to_numeric(df_cat["count"])
st.bar_chart(df_cat, x="category_name", y="count", x_label="", y_label="")


# Average by month
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

st.subheader("📅 Moyenne mensuelle Order Item Total")
df_month = pd.DataFrame(stats["avg_by_month"])

df_month["shipping_month_name"] = pd.Categorical(
    df_month["shipping_month_name"],
    categories=month_order,
    ordered=True)

df_month = df_month.rename(columns={"avg(order_item_total)": "avg_total"})
st.line_chart(df_month.set_index("shipping_month_name")["avg_total"])

# Total by month
st.subheader("📅 Total mensuelle Order Item Total")
df_month = pd.DataFrame(stats["total_by_month"])

df_month["shipping_month_name"] = pd.Categorical(
    df_month["shipping_month_name"],
    categories=month_order,
    ordered=True)

df_month["count"] = pd.to_numeric(df_month["count"])
st.bar_chart(df_month.set_index("shipping_month_name"))

# Average by shipping mode
st.subheader("🚚 Average par mode de livraison")
df_mode = pd.DataFrame(stats["avg_by_shipping_mode"])
df_mode = df_mode.rename(columns={"avg(order_item_total)": "avg_total"})
df_mode["avg_total"] = pd.to_numeric(df_mode["avg_total"])
st.bar_chart(df_mode.set_index("shipping_mode"))

# Count by segment
st.subheader("👥 Clients par segment")
df_segment = pd.DataFrame(stats["count_by_customer_segment"])
df_segment["count"] = pd.to_numeric(df_segment["count"])
st.bar_chart(df_segment.set_index("customer_segment"))