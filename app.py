import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
import altair as alt

# Page config
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# Load Vasena logo (must be named vasena_logo.png in root)
logo = Image.open("vasena_logo.png")
st.image(logo, width=150)

# Branded tagline
st.markdown("""
<div style='text-align: left; font-size:22px; color:#1f2937; font-weight:bold; margin-top: -10px;'>
🔷 Built by Vasena Inc. | Understand who moves your mission.
</div>
""", unsafe_allow_html=True)

# Title
st.title("📊 PartnerIQ: Donor & Partner Intelligence Dashboard")

# Upload Section
uploaded_file = st.file_uploader("📤 Upload your donation or partner data (CSV or Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Ensure date column is datetime
    df['Donation Date'] = pd.to_datetime(df['Donation Date'])

    # Sidebar: Filter by date range
    st.sidebar.header("📅 Filter by Date Range")
    min_date = df['Donation Date'].min().date()
    max_date = df['Donation Date'].max().date()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        df = df[(df['Donation Date'] >= start_date) & (df['Donation Date'] <= end_date)]

    # Aggregate donor data
    summary = df.groupby('Donor Name').agg({
        'Donation Amount': 'sum',
        'Donation Date': 'max',
        'Email': 'first'
    }).reset_index()
    summary.columns = ['Partner Name', 'Total Contributed', 'Last Donation Date', 'Email']

    # Sort by contribution
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

    # Retention Risk
    summary['Days Since Last'] = (datetime.today() - summary['Last Donation Date']).dt.days
    summary['Retention Risk'] = summary['Days Since Last'].apply(
        lambda x: "⚠️ At Risk" if x > 180 else "✅ Healthy"
    )

    # Sort by Tier
    tier_order = {
        "Tier A – High Impact": 1,
        "Tier B – Mid Impact": 2,
        "Tier C – Low Impact": 3
    }
    summary['Tier Rank'] = summary['Tier'].map(tier_order)
    summary = summary.sort_values(by='Tier Rank').drop(columns='Tier Rank')

    # Chart: Tier Breakdown with labels and colors
    tier_counts = summary['Tier'].value_counts().reset_index()
    tier_counts.columns = ['Tier', 'Count']
    tier_color_map = {
        'Tier A – High Impact': '#FFD700',   # Gold
        'Tier B – Mid Impact': '#2E8B57',    # Green
        'Tier C – Low Impact': '#F4C430'     # Yellow
    }
    tier_counts['Tier'] = pd.Categorical(tier_counts['Tier'], categories=list(tier_color_map.keys()), ordered=True)
    tier_counts = tier_counts.sort_values('Tier')

    bar_chart = alt.Chart(tier_counts).mark_bar().encode(
        x=alt.X('Tier:N', sort=list(tier_color_map.keys()), axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Count:Q'),
        color=alt.Color('Tier:N', scale=alt.Scale(domain=list(tier_color_map.keys()),
                                                  range=list(tier_color_map.values())),
                        legend=alt.Legend(title="Donor Tiers"))
    ).properties(
        title='Tier Breakdown',
        width=600,
        height=400
    )

    text = alt.Chart(tier_counts).mark_text(
        align='center',
        baseline='middle',
        dy=3,
        color='white',
        fontSize=14,
        fontWeight='bold'
    ).encode(
        x=alt.X('Tier:N', sort=list(tier_color_map.keys())),
        y='Count:Q',
        text='Tier:N'
    )

    st.altair_chart(bar_chart + text, use_container_width=True)

    # Retention Risk Legend
    st.markdown("### 🟨 Retention Risk Legend")
    st.markdown("""
    - ⚠️ **At Risk**: Last donation was more than **180 days ago**  
    - ✅ **Healthy**: Last donation was within **180 days**
    """)

    # Table
    st.subheader("📋 Partner Table")
    st.dataframe(summary, use_container_width=True)

    # Download button
    csv_download = summary.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download PartnerIQ Report", csv_download, "partneriq_report.csv", "text/csv")

else:
    st.info("👆 Upload your CSV or Excel file to get started.")

# Footer
st.markdown("---", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size:18px; color:#1f2937; font-weight:bold;'>
🔷 Built by Vasena Inc. | Understand who moves your mission.
</div>
""", unsafe_allow_html=True)

