import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Analisis E-Commerce",
    layout="wide"
)

sns.set(style="whitegrid")


@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent

    orders_df = pd.read_csv(BASE_DIR / "orders_dataset.csv")
    reviews_df = pd.read_csv(BASE_DIR / "order_reviews_dataset.csv")
    payments_df = pd.read_csv(BASE_DIR / "order_payments_dataset.csv")

    # convert datetime
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ] 
for col in date_cols:
    orders_df[col]=pd.to_datetime(orders_df[col], errors="coerce") 

    # filter tanggal
    orders_df = orders_df[
        (orders_df["order_purchase_timestamp"] >= "2016-09-01") &
        (orders_df["order_purchase_timestamp"] <= "2018-08-31")
    ]

    orders_rfm_df = orders_df.copy() 

    
    orders_df = orders_df.dropna(subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ])

    # delivery status
    orders_df["delivery_status"] = np.where(
        orders_df["order_delivered_customer_date"] <=
        orders_df["order_estimated_delivery_date"],
        "On Time",
        "Late"
    )


    # filter review score valid
    reviews_df = reviews_df[
        reviews_df["review_score"].between(1, 5)
    ]

    # create date column
    orders_df["order_date"] = orders_df["order_purchase_timestamp"].dt.date
    orders_rfm_df["order_date"] = orders_rfm_df["order_purchase_timestamp"].dt.date
    return orders_df, reviews_df, payments_df, orders_rfm_df


orders_df, reviews_df, payments_df, orders_rfm_df = load_data()


st.title("📊 Dashboard Analisis E-Commerce")
st.caption("Berdasarkan Pertanyaan Bisnis Submission Dicoding")

st.sidebar.header("Filter Dashboard")

min_date = orders_df["order_date"].min()
max_date = orders_df["order_date"].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered_orders = orders_df[
    (orders_df["order_date"] >= start_date) &
    (orders_df["order_date"] <= end_date)
]

filtered_rfm = orders_rfm_df[
    (orders_rfm_df["order_date"] >= start_date) &
    (orders_rfm_df["order_date"] <= end_date)
]


st.subheader("Ringkasan Data")

total_orders = filtered_orders["order_id"].nunique()

late_orders = filtered_orders[
    filtered_orders["delivery_status"] == "Late"
]["order_id"].nunique()

late_percent = (late_orders / total_orders) * 100 if total_orders > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Late Orders", f"{late_orders:,}")
col3.metric("Late Percentage", f"{late_percent:.2f}%")


st.header("1️⃣ Pengaruh Keterlambatan terhadap Review Score")

review_order_df = pd.merge(
    filtered_orders[["order_id", "delivery_status"]],
    reviews_df[["order_id", "review_score"]],
    on="order_id",
    how="inner"
)

avg_review = review_order_df.groupby(
    "delivery_status"
)["review_score"].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=avg_review, x="delivery_status", y="review_score", ax=ax)
ax.set_title("Rata-rata Review Score")
st.pyplot(fig)


st.header("2️⃣ Metode Pembayaran Paling Dominan")

payment_summary = payments_df.groupby("payment_type").agg({
    "order_id": "count",
    "payment_value": "sum"
}).reset_index()

payment_summary.columns = [
    "payment_type",
    "total_transaction",
    "total_revenue"
]

payment_summary = payment_summary.sort_values(
    by="total_revenue",
    ascending=False
)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=payment_summary, x="payment_type", y="total_transaction", ax=ax)
plt.xticks(rotation=30)
ax.set_title("Jumlah Transaksi per Payment Type")
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=payment_summary, x="payment_type", y="total_revenue", ax=ax)
plt.xticks(rotation=30)
ax.set_title("Total Revenue per Payment Type")
st.pyplot(fig)

top_payment = payment_summary.iloc[0]["payment_type"]

st.info(f"Metode pembayaran paling dominan adalah **{top_payment}**.")


st.header("3️⃣ Segmentasi Pelanggan (RFM)")

rfm_df = pd.merge(
    filtered_rfm[["order_id", "customer_id", "order_purchase_timestamp"]],
    payments_df[["order_id", "payment_value"]],
    on="order_id",
    how="inner"
)

rfm_df = rfm_df.groupby("customer_id").agg({
    "order_purchase_timestamp": "max",
    "order_id": "nunique",
    "payment_value": "sum"
}).reset_index()

rfm_df.columns = [
    "customer_id",
    "last_order",
    "frequency",
    "monetary"
]

recent_date = filtered_rfm["order_purchase_timestamp"].max()

rfm_df["recency"] = (recent_date - rfm_df["last_order"]).dt.days

rfm_df["segment"] = np.where(
    (rfm_df["frequency"] >= 3) & (rfm_df["monetary"] >= 300),
    "Best Customer",
    np.where(
        rfm_df["recency"] > 180,
        "Lost Customer",
        "Regular Customer"
    )
)

segment_count = rfm_df["segment"].value_counts().reset_index()
segment_count.columns = ["segment", "total_customer"]

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=segment_count, x="segment", y="total_customer", ax=ax)
ax.set_title("Jumlah Pelanggan per Segmen")
st.pyplot(fig)

st.info("Best Customer perlu dipertahankan, Lost Customer perlu diaktivasi kembali.")


st.header("📌 Kesimpulan")

st.markdown("""
- Pesanan tepat waktu memiliki review lebih baik.
- Metode pembayaran tertentu mendominasi transaksi.
- Mayoritas pelanggan adalah Regular Customer.
- Ada segmen Best Customer yang penting untuk bisnis.
""")

st.header("🚀 Rekomendasi")

st.markdown("""
1. Tingkatkan logistik agar tidak terlambat.
2. Optimalkan metode pembayaran dominan.
3. Berikan reward untuk Best Customer.
4. Reaktivasi Lost Customer.
""")


