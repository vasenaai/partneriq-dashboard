import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# Set page config
st.set_page_config(layout="wide")

# Logo and Header
st.image("vasena_logo.png", width=120)
st.markdown(
    "<h4 style='color:#00008B;'>🔷 Built by Vasena Inc. | Understand who moves your mission.</h4>",
    unsafe_allow_html=True,
)

st.markdown("## 📊 PartnerIQ: Donor & Partner Intelligence Dashboard")

# File Upload
uploaded_file = st.file_uploader("📥 Upload your donation or partner data (CSV or Excel)", type=["csv", "xlsx"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean and derive data
    df['Last Donation Date'] = pd.to_datetime(df['Last Donation Date'])
    df['Days Since Last'] = (datetime.now() - df['Last Donation Date']).dt.days
    df['Retention Risk'] = df['Days Since Last'].apply(lambda x: '⚠️ At Risk' if x > 180 else '✅ Healthy')

    def categorize_tier(amount):
        if amount >= 5000:
            return 'Tier A – High Impact'
        elif amount >= 1000:
            return 'Tier B – Mid Impact'
        else:
            return 'Tier C – Low Impact'

    df['Tier'] = df['Total Contributed'].apply(categorize_tier)

    # Chart Data
    tier_counts = df['Tier'].value_counts().reindex([
        'Tier A – High Impact', 'Tier B – Mid Impact', 'Tier C – Low Impact'
    ]).fillna(0)

    # Chart colors
    color_map = {
        'Tier A – High Impact': '#2E8B57',  # Green
        'Tier B – Mid Impact': '#4682B4',   # Blue
        'Tier C – Low Impact': '#87CEEB'    # Light Blue
    }

    # Draw chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(tier_counts.index, tier_counts.values, color=[color_map[t] for t in tier_counts.index])

    for bar, label in zip(bars, tier_counts.index):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height/2, label,
                ha='center', va='center', color='white', fontsize=10, fontweight='bold')

    ax.set_ylabel("Count")
    ax.set_title("Tier Breakdown")
    ax.set_ylim(0, max(tier_counts.values) + 1)
    ax.set_xlabel("")

    st.pyplot(fig)

    # Table
    st.markdown("## 🗂 Partner Table")
    df_sorted = df.sort_values(by='Total Contributed', ascending=False).reset_index(drop=True)
    st.dataframe(df_sorted[['Partner Name', 'Total Contributed', 'Last Donation Date', 'Email', 'Tier', 'Days Since Last', 'Retention Risk']])

