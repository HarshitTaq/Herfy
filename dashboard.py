import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard", layout="wide")
st.title("📋 Auditor Completion Dashboard")

# Load Excel from current directory
file_path = "CLEANLINESS AUDIT.xlsx"
sheet_name = "CLEANLINESS_AUDIT"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # --- Extract Section 1: Expected ---
    expected_df = df.iloc[:, [0, 1]].dropna()
    expected_df.columns = ["Name", "Expected"]

    # --- Extract Section 2: Actual ---
    actual_df = df.iloc[:, [5, 6]].dropna()
    actual_df.columns = ["Store", "Actual"]

    # Count how many stores each OC covered
    actual_counts = actual_df["Actual"].value_counts().reset_index()
    actual_counts.columns = ["Name", "Actual"]

    # --- Merge & calculate missed ---
    merged_df = expected_df.merge(actual_counts, on="Name", how="left")
    merged_df["Actual"] = merged_df["Actual"].fillna(0).astype(int)
    merged_df["Missed Submissions of assigned OC"] = merged_df["Expected"] - merged_df["Actual"]

    # --- Sort & Limit to Top 32 ---
    merged_df = merged_df.sort_values("Name").reset_index(drop=True)
    merged_df.index += 1  # Start from 1
    merged_df = merged_df.iloc[:32]

    # --- Summary Row ---
    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Expected": [merged_df["Expected"].sum()],
        "Actual": [merged_df["Actual"].sum()],
        "Missed Submissions of assigned OC": [merged_df["Missed Submissions of assigned OC"].sum()]
    }, index=[""])

    final_df = pd.concat([merged_df, total_row], axis=0)

    # --- Show Table ---
    st.subheader("📊 Completion Summary (First 32 Auditors)")
    st.dataframe(final_df, use_container_width=True)

    # --- Show Bar Chart ---
    st.subheader("📈 Expected vs Actual Submissions")
    fig = px.bar(
        merged_df,
        x="Name",
        y=["Expected", "Actual"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(range=[0, 20]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Something went wrong: {e}")

st.markdown("## 🔍 Store Submission Tracker by OC")

# Get unique auditors from projected
ocs = projected_df['Projected'].dropna().unique()
selected_oc = st.selectbox("Select an Auditor (OC)", sorted(ocs))

# Get all projected stores for selected OC
projected_stores = projected_df[projected_df['Projected'] == selected_oc]['Store'].tolist()

# Get all actual stores submitted by this OC
actual_stores = actual_df[actual_df['Actual'] == selected_oc]['Store'].tolist()

# Create table with submission status
status_table = pd.DataFrame({
    "Projected Stores": projected_stores,
    "Submitted Stores": [store if store in actual_stores else "" for store in projected_stores],
    "Submission Status": ["✅ Submitted" if store in actual_stores else "❌ Missing" for store in projected_stores]
})

# Display result
st.dataframe(status_table, use_container_width=True)

