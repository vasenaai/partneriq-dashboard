import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# Load and display the logo once
st.image("logo.png", width=80)  # Ensure logo.png is in the same folder

# Horizontal header
col1, _ = st.columns([12, 1])
with col1:
    st.markdown(
        "<span style='font-size: 18px;'>🔷 <strong>Built by Vasena Inc.</strong> | Understand who moves your mission.<br>📊 PartnerIQ: Donor & Partner Intelligence Dashboard</span>",
        unsafe_allow_html=True,
    )

# File upload
st.markdown("Upload your donor file (CSV or Excel)")
uploaded_file = st.file_uploader(" ", type=["csv", "xlsx"])

if uploaded_file:
    # Read data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    required_columns = {"Name", "Donation"}
    if not required_columns.issubset(df.columns):
        st.error("The file must contain 'Name' and 'Donation' columns.")
    else:
        # Assign tiers
        def assign_tier(amount):
            if amount >= 10000:
                return "Tier A - High Impact"
            elif amount >= 1000:
                return "Tier B - Mid Impact"
            else:
                return "Tier C - Low Impact"

        df["Impact Tier"] = df["Donation"].apply(assign_tier)

        # Chart data
        tier_counts = df["Impact Tier"].value_counts().reindex(
            ["Tier A - High Impact", "Tier B - Mid Impact", "Tier C - Low Impact"]
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(8, 4))
        colors = ["seagreen", "steelblue", "skyblue"]
        bars = ax.bar(range(len(tier_counts)), tier_counts.values, color=colors)

        # Add tier label + count inside each bar
        for idx, bar in enumerate(bars):
            height = bar.get_height()
            label = f"{tier_counts.index[idx]}\n{int(height)}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height / 2,
                label,
                ha="center",
                va="center",
                fontsize=9,
                color="white",
                weight="bold",
            )

        ax.set_ylabel("Number of Donors")
        ax.set_xticks([])  # Remove x-axis labels
        ax.set_title("Donor Distribution by Impact Tier", fontsize=14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig)

        # Donor list
        st.markdown("### 🧾 Donor List Sorted by Donation Amount")
        sorted_df = df.sort_values(by="Donation", ascending=False)[
            ["Name", "Donation", "Impact Tier"]
        ]
        st.dataframe(sorted_df, use_container_width=True)
