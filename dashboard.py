import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard", layout="wide")
st.title("📋 Auditor Completion Dashboard")

# ----------------- CLEANLINESS -----------------
st.header("🧼 1. CLEANLINESS AUDIT (Q1 - March to 10th July)")

try:
    df = pd.read_excel("CLEANLINESS AUDIT.xlsx", sheet_name="CLEANLINESS_AUDIT")

    expected_df = df.iloc[:, [0, 1]].dropna()
    expected_df.columns = ["Name", "Expected"]

    actual_df = df.iloc[:, [5, 6]].dropna()
    actual_df.columns = ["Store", "Actual"]

    actual_counts = actual_df["Actual"].value_counts().reset_index()
    actual_counts.columns = ["Name", "Actual"]

    merged_df = expected_df.merge(actual_counts, on="Name", how="left")
    merged_df["Actual"] = merged_df["Actual"].fillna(0).astype(int)
    merged_df["Missed Submissions of assigned OC"] = merged_df["Expected"] - merged_df["Actual"]

    merged_df = merged_df.sort_values("Name").reset_index(drop=True)
    merged_df.index += 1
    merged_df = merged_df.iloc[:32]

    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Expected": [merged_df["Expected"].sum()],
        "Actual": [merged_df["Actual"].sum()],
        "Missed Submissions of assigned OC": [merged_df["Missed Submissions of assigned OC"].sum()]
    }, index=[""])

    final_df = pd.concat([merged_df, total_row], axis=0)

    st.subheader("📊 Completion Table")
    st.dataframe(final_df, use_container_width=True)

    fig = px.bar(
        merged_df, 
        x="Name", 
        y=["Expected", "Actual"],
        barmode="group", 
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True, key="clean_bar")

    # Completion % Table + Chart
    with st.expander("📊 Show Completion % - Cleanliness"):
        pct_df = merged_df[["Name", "Expected", "Actual"]].copy()
        pct_df["Completion %"] = (pct_df["Actual"] / pct_df["Expected"] * 100).round(1)
        st.dataframe(pct_df[["Name", "Completion %"]], use_container_width=True)

        fig_pct = px.bar(pct_df, x="Name", y="Completion %", text="Completion %")
        fig_pct.update_layout(
            xaxis_tickangle=-45,
            yaxis=dict(title="Completion Rate (%)", range=[0, 110]),
            height=500
        )
        st.plotly_chart(fig_pct, use_container_width=True, key="clean_pct")

    # 🥧 Leader-wise Pie Chart (Cleanliness)
    st.subheader("🥧 Cleanliness Completion by Leader (Expected vs Actual)")

    leader_data = pd.DataFrame({
        "Leader": ["Mr. Albert", "Mr. Said"],
        "Expected": [192, 183],
        "Actual": [103, 123]
    })

    leader_data["Completion %"] = (leader_data["Actual"] / leader_data["Expected"] * 100).round(1)
    leader_data["Label"] = leader_data.apply(
        lambda row: f"{row['Leader']} ({row['Actual']}/{row['Expected']}, {row['Completion %']}%)", axis=1
    )

    fig_pie = px.pie(
        leader_data,
        names="Label",
        values="Actual",
        title="Cleanliness - Leader-wise Actual Completion",
        hole=0.4
    )
    fig_pie.update_traces(textinfo="label+percent", pull=[0.05, 0.05])
    fig_pie.update_layout(height=400, margin=dict(t=50, b=50, l=30, r=30))

    st.plotly_chart(fig_pie, use_container_width=True, key="clean_leader_pie")

except Exception as e:
    st.error(f"Cleanliness Error: {e}")


# ----------------- CRO -----------------
st.header("🏪 2. CRO (Capturing Restaurant Opportunity) AUDIT (Yearly)")

try:
    cro_actual = pd.read_excel("CRO AUDIT.xlsx", sheet_name="CRO_ACTUAL")
    cro_projected = pd.read_excel("CRO AUDIT.xlsx", sheet_name="CRO_PROJECTED")

    cro_merged = pd.merge(cro_projected, cro_actual, on="Store", how="outer")
    cro_merged = cro_merged[["Store", "Projected", "Actual"]]

    proj_counts = cro_merged["Projected"].value_counts().reset_index()
    proj_counts.columns = ["Name", "Projected_Stores"]

    act_counts = cro_merged["Actual"].value_counts().reset_index()
    act_counts.columns = ["Name", "Actual_Stores"]

    cro_summary = pd.merge(proj_counts, act_counts, on="Name", how="outer").fillna(0)
    cro_summary[["Projected_Stores", "Actual_Stores"]] = cro_summary[["Projected_Stores", "Actual_Stores"]].astype(int)
    cro_summary["Missed Submissions of Assigned OC"] = cro_summary["Projected_Stores"] - cro_summary["Actual_Stores"]

    cro_summary = cro_summary.sort_values("Name").reset_index(drop=True)
    cro_summary.index += 1

    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Projected_Stores": [cro_summary["Projected_Stores"].sum()],
        "Actual_Stores": [cro_summary["Actual_Stores"].sum()],
        "Missed Submissions of Assigned OC": [cro_summary["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    cro_final = pd.concat([cro_summary, total_row], axis=0)

    st.subheader("📊 Completion Table")
    st.dataframe(cro_final, use_container_width=True)

    fig = px.bar(
        cro_summary, 
        x="Name", 
        y=["Projected_Stores", "Actual_Stores"], 
        barmode="group", 
        text_auto=True
    )
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True, key="cro_bar")

    # Completion % Table + Chart
    with st.expander("📊 Show Completion % - CRO"):
        pct_df = cro_summary[["Name", "Projected_Stores", "Actual_Stores"]].copy()
        pct_df["Completion %"] = (pct_df["Actual_Stores"] / pct_df["Projected_Stores"] * 100).round(1)
        st.dataframe(pct_df[["Name", "Completion %"]], use_container_width=True)

        fig_pct = px.bar(pct_df, x="Name", y="Completion %", text="Completion %")
        fig_pct.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 110], height=500)
        st.plotly_chart(fig_pct, use_container_width=True, key="cro_pct")

    # 🥧 Leader-wise Pie Chart (with expected vs actual)
    st.subheader("🥧 CRO Completion by Leader (Expected vs Actual)")

    leader_data = pd.DataFrame({
        "Leader": ["Mr. Albert", "Mr. Said"],
        "Expected": [192, 183],
        "Actual": [144, 106]
    })

    leader_data["Completion %"] = (leader_data["Actual"] / leader_data["Expected"] * 100).round(1)
    leader_data["Label"] = leader_data.apply(
        lambda row: f"{row['Leader']} ({row['Actual']}/{row['Expected']}, {row['Completion %']}%)", axis=1
    )

    fig_pie = px.pie(
        leader_data,
        names="Label",
        values="Actual",
        title="CRO - Leader-wise Actual Completion",
        hole=0.4
    )
    fig_pie.update_traces(textinfo="label+percent", pull=[0.05, 0.05])
    fig_pie.update_layout(height=400, margin=dict(t=50, b=50, l=30, r=30))

    st.plotly_chart(fig_pie, use_container_width=True, key="cro_leader_pie")

except Exception as e:
    st.error(f"CRO Error: {e}")

# ----------------- IDEAL -----------------
st.header("📦 3. IDEAL STORE GUIDE - VM (Yearly)")
try:
    df_ideal = pd.read_excel("IDEAL AUDIT.xlsx", sheet_name="IDEAL_AUDIT")
    df_ideal = df_ideal.rename(columns={"Delta": "Missed Submissions of Assigned OC"})
    df_ideal = df_ideal[df_ideal["Name"].notna() & (df_ideal["Name"].astype(str).str.strip() != "")]
    df_ideal[["Expected", "Actual", "Missed Submissions of Assigned OC"]] = df_ideal[[
        "Expected", "Actual", "Missed Submissions of Assigned OC"
    ]].fillna(0).astype(int)

    df_ideal = df_ideal.sort_values("Name").reset_index(drop=True)
    df_ideal.index += 1

    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Expected": [df_ideal["Expected"].sum()],
        "Actual": [df_ideal["Actual"].sum()],
        "Missed Submissions of Assigned OC": [df_ideal["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    df_final = pd.concat([df_ideal, total_row], axis=0)

    st.subheader("📊 Completion Table")
    st.dataframe(df_final, use_container_width=True)

    fig = px.bar(df_ideal, x="Name", y=["Expected", "Actual"], barmode="group", text_auto=True)
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True, key="ideal_bar")

    with st.expander("📊 Show Completion % - IDEAL"):
        pct_df = df_ideal[["Name", "Expected", "Actual"]].copy()
        pct_df["Completion %"] = (pct_df["Actual"] / pct_df["Expected"] * 100).round(1)
        st.dataframe(pct_df[["Name", "Completion %"]], use_container_width=True)

        fig_pct = px.bar(pct_df, x="Name", y="Completion %", text="Completion %")
        fig_pct.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 110], height=500)
        st.plotly_chart(fig_pct, use_container_width=True, key="ideal_pct")

except Exception as e:
    st.error(f"IDEAL Error: {e}")

# ----------------- QSC -----------------
st.header("📋 4. QSC AUDIT (Monthly) - Month-wise Summary & Completion %")
try:
    xls = pd.ExcelFile("QSC AUDIT.xlsx")
    all_months = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        df["Month"] = sheet
        all_months.append(df)

    qsc_df = pd.concat(all_months, ignore_index=True)
    qsc_df = qsc_df.rename(columns={"Delta": "Missed Submissions of Assigned OC"})
    qsc_df = qsc_df[qsc_df["Name"].notna() & (qsc_df["Name"].astype(str).str.strip() != "")]
    qsc_df[["Expected", "Actual", "Missed Submissions of Assigned OC"]] = qsc_df[[
        "Expected", "Actual", "Missed Submissions of Assigned OC"
    ]].fillna(0).astype(int)

    month_order = ["Jan", "Feb", "March", "April", "May", "June", "July"]
    qsc_df["Month"] = pd.Categorical(qsc_df["Month"], categories=month_order, ordered=True)

    selected_month = st.selectbox("🗓 Select Month", options=month_order)
    df_month = qsc_df[qsc_df["Month"] == selected_month].copy()
    df_month = df_month.sort_values("Name").reset_index(drop=True)
    df_month.index += 1

    total_row = pd.DataFrame({
        "Month": [selected_month],
        "Name": ["Total"],
        "Expected": [df_month["Expected"].sum()],
        "Actual": [df_month["Actual"].sum()],
        "Missed Submissions of Assigned OC": [df_month["Missed Submissions of Assigned OC"].sum()]
    }, index=[""])

    df_final = pd.concat([df_month, total_row], axis=0)

    st.subheader(f"📊 QSC Table - {selected_month}")
    st.dataframe(df_final.drop(columns=["Month"]), use_container_width=True)

    st.subheader(f"📊 QSC Audit Chart - {selected_month}")
    fig = px.bar(df_month, x="Name", y=["Expected", "Actual"], barmode="group", text_auto=True)
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True, key="qsc_bar")

    with st.expander(f"📊 Show Completion % - QSC ({selected_month})"):
        pct_df = df_month[["Name", "Expected", "Actual"]].copy()
        pct_df["Completion %"] = (pct_df["Actual"] / pct_df["Expected"] * 100).round(1)
        st.dataframe(pct_df[["Name", "Completion %"]], use_container_width=True)

        fig_pct = px.bar(pct_df, x="Name", y="Completion %", text="Completion %")
        fig_pct.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 110], height=500)
        st.plotly_chart(fig_pct, use_container_width=True, key="qsc_pct")

except Exception as e:
    st.error(f"QSC Error: {e}")
