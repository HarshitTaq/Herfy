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

# ----------------- IDEAL Process Dashboard (Clean with Excel total row excluded) -----------------

st.header("📋 IDEAL Audit - Final Summary (from IDEAL_AUDIT sheet)")

try:
    df_ideal = pd.read_excel("IDEAL AUDIT.xlsx", sheet_name="IDEAL_AUDIT")
    df_ideal = df_ideal[["Name", "Expected", "Actual", "Delta"]]
    df_ideal = df_ideal.rename(columns={"Delta": "Missed Submissions of Assigned OC"})

    # ❗ Drop Excel's total row — where Name is blank or NaN
    df_ideal = df_ideal[df_ideal["Name"].notna() & (df_ideal["Name"].astype(str).str.strip() != "")]

    # Fill NaNs before converting
    df_ideal[["Expected", "Actual", "Missed Submissions of Assigned OC"]] = df_ideal[
        ["Expected", "Actual", "Missed Submissions of Assigned OC"]
    ].fillna(0).astype(int)

    df_ideal = df_ideal.sort_values("Name").reset_index(drop=True)
    df_ideal.index += 1

    # Our own total row (correct one)
    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Expected": [df_ideal["Expected"].sum()],
        "Actual": [df_ideal["Actual"].sum()],
        "Missed Submissions of Assigned OC": [df_ideal["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    df_final = pd.concat([df_ideal, total_row], axis=0)

    st.subheader("📊 IDEAL Completion Table")
    st.dataframe(df_final, use_container_width=True)

    st.subheader("📈 IDEAL Audit Chart")
    fig_ideal = px.bar(
        df_ideal,
        x="Name",
        y=["Expected", "Actual"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig_ideal.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(title="Stores", range=[0, df_ideal[["Expected", "Actual"]].max().max() + 2]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(fig_ideal, use_container_width=True)

except Exception as e:
    st.error(f"IDEAL Error: {e}")

# ----------------- QSC Process Dashboard (with Month Filter) -----------------

# ----------------- QSC Process Dashboard (Simplified & Final) -----------------

st.header("📋 QSC Audit - Projected vs Actual (Month-wise Summary)")

try:
    import pandas as pd
    import plotly.express as px

    # Load all sheets from Excel and tag with Month
    qsc_path = "QSC AUDIT.xlsx"
    xls = pd.ExcelFile(qsc_path)

    all_months = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        df["Month"] = sheet
        all_months.append(df)

    qsc_df = pd.concat(all_months, ignore_index=True)

    # Clean and rename
    qsc_df = qsc_df.rename(columns={"Delta": "Missed Submissions of Assigned OC"})
    qsc_df = qsc_df[qsc_df["Name"].notna() & (qsc_df["Name"].astype(str).str.strip() != "")]
    qsc_df[["Expected", "Actual", "Missed Submissions of Assigned OC"]] = qsc_df[
        ["Expected", "Actual", "Missed Submissions of Assigned OC"]
    ].fillna(0).astype(int)

    # Sort months in correct order
    month_order = ["Jan", "Feb", "March", "April", "May", "June", "July"]
    qsc_df["Month"] = pd.Categorical(qsc_df["Month"], categories=month_order, ordered=True)

    # Month dropdown (multi-select)
    selected_months = st.multiselect(
        "📅 Select Month(s)", options=month_order,
        default=["Jan"]
    )

    df_filtered = qsc_df[qsc_df["Month"].isin(selected_months)].copy()
    df_filtered = df_filtered.sort_values(["Month", "Name"]).reset_index(drop=True)
    df_filtered.index += 1

    # Summary row (total at bottom)
    total_row = pd.DataFrame({
        "Month": ["Total"],
        "Name": ["Total"],
        "Expected": [df_filtered["Expected"].sum()],
        "Actual": [df_filtered["Actual"].sum()],
        "Missed Submissions of Assigned OC": [df_filtered["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    df_final = pd.concat([df_filtered, total_row], axis=0)

    # Display Table
    st.subheader("📊 Completion Table")
    st.dataframe(df_final.drop(columns=["Month"]), use_container_width=True)

    # Display Bar Chart (simple)
    st.subheader("📈 Audit Chart")
    fig = px.bar(
        df_filtered,
        x="Name",
        y=["Expected", "Actual"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(title="Stores", range=[0, df_filtered[["Expected", "Actual"]].max().max() + 2]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"QSC Error: {e}")

