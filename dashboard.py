import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard", layout="wide")
st.title("📋 Auditor Completion Dashboard")

# File name and sheet name
excel_file = "CLEANLINESS AUDIT.xlsx"
sheet_name = "CLEANLINESS_AUDIT"

try:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # --- Extract sections from consolidated columns ---
    expected_df = df.iloc[:, [0, 1]].copy()
    expected_df.columns = ["Name", "Expected"]

    actual_raw = df.iloc[:, [5, 6]].dropna().copy()
    actual_raw.columns = ["Store", "Auditor"]

    projected_raw = df.iloc[:, [8, 9]].dropna().copy()
    projected_raw.columns = ["Store", "Auditor"]

    # --- Calculate actual counts per auditor ---
    actual_counts = actual_raw["Auditor"].value_counts().reset_index()
    actual_counts.columns = ["Name", "Actual"]

    # --- Merge with expected ---
    merged = expected_df.merge(actual_counts, on="Name", how="left")
    merged["Actual"] = merged["Actual"].fillna(0).astype(int)
    merged["Delta"] = (merged["Expected"] - merged["Actual"]).abs()

    st.subheader("🧾 Auditor Completion Summary (Cleanliness Audit)")
    st.dataframe(merged.sort_values("Name"), use_container_width=True)

    # --- Plot bar chart ---
    fig = px.bar(
        merged.sort_values("Expected", ascending=False),
        x="Name",
        y=["Expected", "Actual"],
        barmode="group",
        title="Auditor Completion - CLEANLINESS AUDIT",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig.update_layout(xaxis_tickangle=-45, height=500, margin=dict(l=20, r=20, t=50, b=100))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
