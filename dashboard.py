
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard", layout="wide")

st.markdown("""
    <style>
    [data-testid="stExpander"] > div:first-child {
        background-color: #ffe6e6;
        color: black;
        border-radius: 8px;
        font-weight: 600;
    }
    [data-testid="stExpander"] > div:first-child:hover {
        background-color: #ffcccc;
    }
    </style>
    """, unsafe_allow_html=True)

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
    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Expected": [merged_df["Expected"].sum()],
        "Actual": [merged_df["Actual"].sum()],
        "Missed Submissions of assigned OC": [merged_df["Missed Submissions of assigned OC"].sum()]
    }, index=[""])
    final_df = pd.concat([merged_df, total_row], axis=0)
    st.subheader("📊 Completion Table")
    st.dataframe(final_df, use_container_width=True)
    fig = px.bar(merged_df, x="Name", y=["Expected", "Actual"], barmode="group", text_auto=True)
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True, key="clean_bar")

    with st.expander("📊 Show Completion % - Cleanliness"):
        pct_df = merged_df[["Name", "Expected", "Actual"]].copy()
        pct_df["Completion %"] = (pct_df["Actual"] / pct_df["Expected"] * 100).round(1)
        st.dataframe(pct_df[["Name", "Completion %"]], use_container_width=True)
        fig_pct = px.bar(pct_df, x="Name", y="Completion %", text="Completion %")
        fig_pct.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 110], height=500)
        st.plotly_chart(fig_pct, use_container_width=True, key="clean_pct")

    st.subheader("🥧 Cleanliness Completion by Leader (Expected vs Actual)")
    pie_data = pd.DataFrame({
        "Leader": ["Mr. Albert", "Mr. Said"],
        "Expected": [192, 183],
        "Actual": [103, 123]
    })
    pie_data["Completion %"] = (pie_data["Actual"] / pie_data["Expected"] * 100).round(1)
    pie_data["Label"] = pie_data.apply(lambda row: f"{row['Leader']} ({row['Actual']}/{row['Expected']}, {row['Completion %']}%)", axis=1)
    pie_fig = px.pie(pie_data, names="Label", values="Actual", title="Cleanliness - Leader-wise Actual Completion", hole=0.4)
    pie_fig.update_traces(textinfo="label+percent", pull=[0.05, 0.05])
    pie_fig.update_layout(height=400)
    st.plotly_chart(pie_fig, use_container_width=True, key="clean_leader_pie")

except Exception as e:
    st.error(f"Cleanliness Error: {e}")
