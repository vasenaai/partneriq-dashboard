import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import os
import streamlit as st

# Check if logo file exists
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=80)
else:
    st.markdown("🔷 Built by Vasena Inc. | Understand who moves your mission.", unsafe_allow_html=True)

# Page setup
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# Header with logo and subtitle
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=80)  # Replace with your logo filename
with col2:
    st.markdown("### 🔷 Built by Vasena Inc. | Understand who moves your mission.\n📊 PartnerIQ: Donor & Partner Intelligence Dashboard")

# Upload data
uploaded_file = st.file_uploader("Upload your donor file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Format donation date
    df['Donation Date'] = pd.to_datetime(df['Donation Date'], errors='coerce')

    # Assign tiers
    def assign_tier(row):
        if row['Total Donation'] >= 10000:
            return "Tier A - High Impact"
        elif row['Total Donation'] >= 1000:
            return "Tier B - Mid Impact"
        else:
            return "Tier C - Low Impact"

    df['Impact Tier'] = df.apply(assign_tier, axis=1)

    # Tier distribution chart
    tier_counts = df['Impact Tier'].value_counts()
    colors = {
        "Tier A - High Impact": "#2E8B57",
        "Tier B - Mid Impact": "#4682B4",
        "Tier C - Low Impact": "#87CEEB"
    }

    fig, ax = plt.subplots()
    bars = ax.bar(tier_counts.index, tier_counts.values, color=[colors.get(tier, "#888") for tier in tier_counts.index])
    ax.set_title("Donor Distribution by Impact Tier", fontsize=16, pad=20)
    ax.set_ylabel("Number of Donors")
    ax.set_xlabel("")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height, f'{int(height)}', ha='center', va='bottom', fontsize=12)

    st.pyplot(fig)

    # Donor table sorted by donation amount (High to Low)
    df_sorted = df.sort_values(by='Total Donation', ascending=False)

    st.subheader("📋 Donor List (Sorted by Donation Amount)")
    st.dataframe(df_sorted[['Donor Name', 'Total Donation', 'Donation Date', 'Campaign', 'Email', 'Impact Tier']])

else:
    st.warning("📁 Please upload a donor data file to proceed.")
