import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

# Set page config
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# --- Header with logo and captions ---
logo = Image.open("vasena_logo.png")  # Make sure your logo is saved with this name
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=100)
with col2:
    st.markdown("""
    <div style="padding-top: 20px;">
        <span style="font-weight: bold; color: #0a58ca;">🔷 Built by Vasena Inc. | Understand who moves your mission.</span><br>
        <span style="font-size: 20px; font-weight: 600;">📊 PartnerIQ: Donor & Partner Intelligence Dashboard</span>
    </div>
    """, unsafe_allow_html=True)

# --- File upload ---
uploaded_file = st.file_uploader("Upload Donor Data (.csv)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Clean & prepare data ---
    df['Donation Date'] = pd.to_datetime(df['Donation Date'], errors='coerce')

    # Assign Impact Tier
    def assign_tier(row):
        if row['Total Donation'] >= 10000:
            return 'Tier A - High Impact'
        elif row['Total Donation'] >= 1000:
            return 'Tier B - Mid Impact'
        else:
            return 'Tier C - Low Impact'

    df['Impact Tier'] = df.apply(assign_tier, axis=1)

    # --- Display Donor Table ---
    with st.expander("📋 View Donor List"):
        st.dataframe(df[['Donor Name', 'Total Donation', 'Donation Date', 'Impact Tier']])

    # --- Summary Chart ---
    tier_counts = df['Impact Tier'].value_counts().reindex([
        'Tier A - High Impact', 'Tier B - Mid Impact', 'Tier C - Low Impact'
    ], fill_value=0)

    tier_colors = {
        'Tier A - High Impact': '#2E8B57',
        'Tier B - Mid Impact': '#4682B4',
        'Tier C - Low Impact': '#1E90FF'
    }

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(tier_counts.index, tier_counts.values,
                  color=[tier_colors[tier] for tier in tier_counts.index])

    for bar, label in zip(bars, tier_counts.index):
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2, height/2, label,
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)

    ax.set_title("📈 Donor Distribution by Impact Tier", fontsize=14)
    ax.set_ylabel("Number of Donors")
    ax.set_xticks([])
    st.pyplot(fig)

    # --- Download Button ---
    csv = df.to_csv(index=False)
    st.download_button("📥 Download Processed Data", data=csv, file_name="processed_donors.csv", mime="text/csv")
