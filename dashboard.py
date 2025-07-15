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


# ----------------- CRO Process Dashboard -----------------

st.header("📋 CRO Audit - Projected vs Actual")

try:
    cro_actual = pd.read_excel("CRO AUDIT.xlsx", sheet_name="CRO_ACTUAL")
    cro_projected = pd.read_excel("CRO AUDIT.xlsx", sheet_name="CRO_PROJECTED")

    cro_merged = pd.merge(
        cro_projected, cro_actual,
        on="Store", how="outer", suffixes=('_Projected', '_Actual')
    )
    cro_merged = cro_merged[['Store', 'Projected', 'Actual']]

    cro_proj_counts = cro_merged['Projected'].value_counts().reset_index()
    cro_proj_counts.columns = ['Name', 'Projected_Stores']

    cro_act_counts = cro_merged['Actual'].value_counts().reset_index()
    cro_act_counts.columns = ['Name', 'Actual_Stores']

    cro_summary = pd.merge(cro_proj_counts, cro_act_counts, on='Name', how='outer').fillna(0)
    cro_summary['Projected_Stores'] = cro_summary['Projected_Stores'].astype(int)
    cro_summary['Actual_Stores'] = cro_summary['Actual_Stores'].astype(int)
    cro_summary["Missed Submissions of Assigned OC"] = cro_summary["Projected_Stores"] - cro_summary["Actual_Stores"]

    cro_summary = cro_summary.sort_values("Name").reset_index(drop=True)
    cro_summary.index += 1

    cro_total = pd.DataFrame({
        "Name": ["Total"],
        "Projected_Stores": [cro_summary["Projected_Stores"].sum()],
        "Actual_Stores": [cro_summary["Actual_Stores"].sum()],
        "Missed Submissions of Assigned OC": [cro_summary["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    cro_final = pd.concat([cro_summary, cro_total], axis=0)

    st.subheader("📊 CRO Completion Table")
    st.dataframe(cro_final, use_container_width=True)

    st.subheader("📈 CRO Audit Chart")
    cro_fig = px.bar(
        cro_summary,
        x="Name",
        y=["Projected_Stores", "Actual_Stores"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    cro_fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(title="Stores", range=[0, cro_summary[["Projected_Stores", "Actual_Stores"]].max().max() + 2]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(cro_fig, use_container_width=True)

except Exception as e:
    st.error(f"CRO Error: {e}")

# ----------------- IDEAL Process Dashboard -----------------

st.header("📋 IDEAL Audit - Projected vs Actual")

try:
    ideal_actual = pd.read_excel("IDEAL AUDIT.xlsx", sheet_name="IDEAL_ACTUAL")
    ideal_projected = pd.read_excel("IDEAL AUDIT.xlsx", sheet_name="IDEAL_PROJECTED")

    ideal_merged = pd.merge(
        ideal_projected, ideal_actual,
        on="Store", how="outer", suffixes=('_Projected', '_Actual')
    )
    ideal_merged = ideal_merged[['Store', 'Projected', 'Actual']]

    ideal_proj_counts = ideal_merged['Projected'].value_counts().reset_index()
    ideal_proj_counts.columns = ['Name', 'Projected_Stores']

    ideal_act_counts = ideal_merged['Actual'].value_counts().reset_index()
    ideal_act_counts.columns = ['Name', 'Actual_Stores']

    ideal_summary = pd.merge(ideal_proj_counts, ideal_act_counts, on='Name', how='outer').fillna(0)
    ideal_summary['Projected_Stores'] = ideal_summary['Projected_Stores'].astype(int)
    ideal_summary['Actual_Stores'] = ideal_summary['Actual_Stores'].astype(int)
    ideal_summary["Missed Submissions of Assigned OC"] = ideal_summary["Projected_Stores"] - ideal_summary["Actual_Stores"]

    ideal_summary = ideal_summary.sort_values("Name").reset_index(drop=True)
    ideal_summary.index += 1

    ideal_total = pd.DataFrame({
        "Name": ["Total"],
        "Projected_Stores": [ideal_summary["Projected_Stores"].sum()],
        "Actual_Stores": [ideal_summary["Actual_Stores"].sum()],
        "Missed Submissions of Assigned OC": [ideal_summary["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    ideal_final = pd.concat([ideal_summary, ideal_total], axis=0)

    st.subheader("📊 IDEAL Completion Table")
    st.dataframe(ideal_final, use_container_width=True)

    st.subheader("📈 IDEAL Audit Chart")
    ideal_fig = px.bar(
        ideal_summary,
        x="Name",
        y=["Projected_Stores", "Actual_Stores"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    ideal_fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(title="Stores", range=[0, ideal_summary[["Projected_Stores", "Actual_Stores"]].max().max() + 2]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(ideal_fig, use_container_width=True)

except Exception as e:
    st.error(f"IDEAL Error: {e}")

