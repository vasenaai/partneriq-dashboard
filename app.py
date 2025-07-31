import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# Logo and header line
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo.png", width=80)  # Make sure logo.png is in the same folder
with col2:
    st.markdown(
        """
        <div style='padding-top: 25px; font-size: 16px;'>
        🔷 Built by <strong>Vasena Inc.</strong> | Understand who moves your mission.
        📊 <strong>PartnerIQ: Donor & Partner Intelligence Dashboard</strong>
        </div>
        """, unsafe_allow_html=True
    )

# Upload file
uploaded_file = st.file_uploader("Upload Donor Data (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Assign tiers based on Donation amount
    def assign_tier(amount):
        if amount >= 5000:
            return "Tier A - High Impact"
        elif amount >= 1000:
            return "Tier B - Mid Impact"
        else:
            return "Tier C - Low Impact"

    df["Impact Tier"] = df["Donation"].apply(assign_tier)

    # Tier summary chart
    st.markdown("### 📊 Donor Distribution by Impact Tier")

    tier_order = ["Tier A - High Impact", "Tier B - Mid Impact", "Tier C - Low Impact"]
    tier_counts = df["Impact Tier"].value_counts().reindex(tier_order, fill_value=0)

    fig, ax = plt.subplots()
    colors = ["seagreen", "steelblue", "skyblue"]
    bars = ax.bar(tier_counts.index, tier_counts.values, color=colors)

    for bar, label in zip(bars, tier_counts.index):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height / 2,
            f"{label}\n{int(height)}",
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            fontweight="bold"
        )

    ax.set_ylabel("Number of Donors")
    ax.set_xticks([])  # Remove x-axis labels
    st.pyplot(fig)

    # Donor list
    st.markdown("### 🧾 Donor List Sorted by Donation Amount")
    sorted_df = df.sort_values(by="Donation", ascending=False)
    st.dataframe(sorted_df, use_container_width=True)
