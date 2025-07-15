import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard - CRO", layout="wide")
st.title("📋 Auditor Completion Dashboard - CRO")

# Load the new Excel file
file_path = "CRO AUDIT.xlsx"

try:
    # Read relevant sheets
    df_actual = pd.read_excel(file_path, sheet_name="CRO_ACTUAL")
    df_projected = pd.read_excel(file_path, sheet_name="CRO_PROJECTED")

    # Merge on Store to match actual vs projected
    merged_df = pd.merge(
        df_projected, df_actual,
        on="Store", how="outer", suffixes=('_Projected', '_Actual')
    )

    # Clean table of Store, Projected (Name), Actual (Name)
    merged_df = merged_df[['Store', 'Projected', 'Actual']]

    # Count how many stores each person was projected for
    projected_counts = merged_df['Projected'].value_counts().reset_index()
    projected_counts.columns = ['Name', 'Projected_Stores']

    # Count how many stores each person actually submitted
    actual_counts = merged_df['Actual'].value_counts().reset_index()
    actual_counts.columns = ['Name', 'Actual_Stores']

    # Merge counts into one table
    summary_df = pd.merge(projected_counts, actual_counts, on='Name', how='outer').fillna(0)
    summary_df['Projected_Stores'] = summary_df['Projected_Stores'].astype(int)
    summary_df['Actual_Stores'] = summary_df['Actual_Stores'].astype(int)

    # Sort alphabetically
    summary_df = summary_df.sort_values("Name").reset_index(drop=True)
    summary_df.index += 1  # start index from 1

    # Summary Row
    total_row = pd.DataFrame({
        "Name": ["Total"],
        "Projected_Stores": [summary_df["Projected_Stores"].sum()],
        "Actual_Stores": [summary_df["Actual_Stores"].sum()],
    }, index=[""])

    final_df = pd.concat([summary_df, total_row], axis=0)

    # Show Table
    st.subheader("📊 Projected vs Actual Store Submissions")
    st.dataframe(final_df, use_container_width=True)

    # Bar Chart (no delta)
    st.subheader("📈 Projected vs Actual Submissions")
    fig = px.bar(
        summary_df,
        x="Name",
        y=["Projected_Stores", "Actual_Stores"],
        barmode="group",
        text_auto=True,
        labels={"value": "Count", "Name": "Auditor"}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis=dict(title="Stores", range=[0, summary_df[["Projected_Stores", "Actual_Stores"]].max().max() + 2]),
        height=500,
        margin=dict(l=20, r=20, t=50, b=100)
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Something went wrong: {e}")

