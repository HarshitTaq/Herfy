import pandas as pd
import streamlit as st
import plotly.express as px

# Upload the Excel file
uploaded_file = st.file_uploader("Upload the CLEANLINESS Excel file", type=["xlsx"])

if uploaded_file:
    # Load the relevant sheets
    audit_df = pd.read_excel(uploaded_file, sheet_name="CLEANLINESS_AUDIT")
    actual_df = pd.read_excel(uploaded_file, sheet_name="CLEANLINESS_ACTUAL")
    projected_df = pd.read_excel(uploaded_file, sheet_name="CLEANLINESS_PROJECTED")

    # Clean up: remove extra spaces if any
    actual_df['Actual'] = actual_df['Actual'].str.strip()
    projected_df['Projected'] = projected_df['Projected'].str.strip()
    audit_df['Name'] = audit_df['Name'].str.strip()

    # Compute expected count from projected
    expected_counts = projected_df['Projected'].value_counts().reset_index()
    expected_counts.columns = ['Name', 'Expected']

    # Compute actual count from actual
    actual_counts = actual_df['Actual'].value_counts().reset_index()
    actual_counts.columns = ['Name', 'Actual']

    # Merge both
    summary_df = pd.merge(expected_counts, actual_counts, on='Name', how='outer').fillna(0)

    # Convert to int
    summary_df['Expected'] = summary_df['Expected'].astype(int)
    summary_df['Actual'] = summary_df['Actual'].astype(int)
    summary_df['Delta'] = (summary_df['Expected'] - summary_df['Actual']).abs()

    # Final Output
    st.subheader("🧾 Auditor Completion Summary - CLEANLINESS")
    st.dataframe(summary_df.sort_values('Name'))

    # 📊 Plot
    fig = px.bar(summary_df.sort_values("Expected", ascending=False),
                 x='Name', y=['Expected', 'Actual'],
                 barmode='group', title="Expected vs Actual Submissions",
                 labels={'value': 'Submission Count', 'Name': 'Auditor'})
    st.plotly_chart(fig, use_container_width=True)
