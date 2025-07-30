import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

st.title("📊 PartnerIQ: Donor & Partner Intelligence Dashboard")
st.caption("Built by Vasena Inc. | Understand who moves your mission.")

# Upload Section
uploaded_file = st.file_uploader("📤 Upload your donation or partner data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Convert dates
    df['Donation Date'] = pd.to_datetime(df['Donation Date'])

    # Sidebar date filter
    st.sidebar.header("📅 Filter by Date Range")
    min_date = df['Donation Date'].min().date()
    max_date = df['Donation Date'].max().date()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        df = df[(df['Donation Date'] >= start_date) & (df['Donation Date'] <= end_date)]

    # Aggregate data
    summary = df.groupby('Donor Name').agg({
        'Donation Amount': 'sum',
        'Donation Date': 'max',
        'Email': 'first'
    }).reset_index()
    summary.columns = ['Partner Name', 'Total Contributed', 'Last Donation Date', 'Email']

    # Sort and classify
    summary = summary.sort_values(by='Total Contributed', ascending=False)
    total_partners = summary.shape[0]
    top_cutoff = int(total_partners * 0.2)

    def assign_tier(index):
        if index < top_cutoff:
            return "Tier A – High Impact"
        elif index < top_cutoff + int(total_partners * 0.3):
            return "Tier B – Mid Impact"
        else:
            return "Tier C – Low Impact"

    summary['Tier'] = [assign_tier(i) for i in range(total_partners)]

    summary['Days Since Last'] = (datetime.today() - summary['Last Donation Date']).dt.days
    summary['Retention Risk'] = summary['Days Since Last'].apply(
        lambda x: "⚠️ At Risk" if x > 180 else "✅ Healthy"
    )

    # Output
    st.subheader("📊 Tier Breakdown")
    st.bar_chart(summary['Tier'].value_counts())

    st.subheader("📋 Partner Table")
    st.dataframe(summary, use_container_width=True)

    csv_download = summary.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download PartnerIQ Report", csv_download, "partneriq_report.csv", "text/csv")

else:
    st.info("👆 Upload your CSV or Excel file to get started.")

# Footer
st.markdown("---")
st.markdown("🔷 **PartnerIQ by Vasena Inc.** | Insight into who moves your mission.")
