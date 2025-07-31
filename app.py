import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="PartnerIQ Dashboard", layout="wide")

# --- HEADER ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("vasena_logo.png", width=90)
with col2:
    st.markdown(
        "<h4 style='margin-bottom:0; color:#00008B;'>"
        "🔷 Built by Vasena Inc. | Understand who moves your mission."
        "</h4>",
        unsafe_allow_html=True
    )

st.markdown(
    "<h1 style='margin-top:0;'>📊 PartnerIQ: Donor & Partner Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("📥 Upload your donation or partner data (CSV or Excel)", type=["csv", "xlsx"])
if not uploaded_file:
    st.stop()

# --- READ FILE ---
if uploaded_file.name.endswith('.csv'):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

# --- CLEAN & PROCESS DATA ---
df.columns = df.columns.str.strip()
if 'Last Donation Date' in df.columns:
    df['Last Donation Date'] = pd.to_datetime(df['Last Donation Date'], errors='coerce')
if 'Total Donation' in df.columns:
    df['Total Donation'] = pd.to_numeric(df['Total Donation'], errors='coerce')

# --- DEFINE SCORING LOGIC ---
def assign_tier(row):
    if row['Total Donation'] >= 10000:
        return 'Tier A - High Impact'
    elif row['Total Donation'] >= 3000:
        return 'Tier B - Mid Impact'
    else:
        return 'Tier C - Low Impact'

df['Impact Tier'] = df.apply(assign_tier, axis=1)

# --- CHART ---
tier_order = ['Tier A - High Impact', 'Tier B - Mid Impact', 'Tier C - Low Impact']
df['Impact Tier'] = pd.Categorical(df['Impact Tier'], categories=tier_order, ordered=True)
tier_counts = df['Impact Tier'].value_counts().reindex(tier_order).fillna(0)

colors = {
    'Tier A - High Impact': '#2E8B57',  # Green
    'Tier B - Mid Impact': '#4682B4',   # Blue
    'Tier C - Low Impact': '#4682B4'    # Blue
}

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(tier_counts.index, tier_counts.values, color=[colors[t] for t in tier_counts.index])

# Add white labels inside bars
for bar, label in zip(bars, tier_counts.index):
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, height / 2, label, ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

ax.set_ylabel("Count")
ax.set_xlabel("")
ax.set_xticks([])
ax.set_title("Tier Breakdown")
st.pyplot(fig)

# --- DONOR TABLE ---
st.markdown("### 🗂️ Partner Table")
df_display = df[['Donor Name', 'Total Donation', 'Impact Tier']].sort_values(by='Total Donation', ascending=False)
st.dataframe(df_display, use_container_width=True)

