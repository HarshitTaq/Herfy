import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title="📋 Auditor Completion Dashboard", layout="wide")
st.title("📋 Auditor Completion Dashboard")

# Automatically detect Excel files in root directory
excel_files = [f for f in os.listdir() if f.endswith(".xlsx")]

if not excel_files:
    st.warning("No Excel files found in the current directory.")
else:
    for file in excel_files:
        try:
            st.subheader(f"📄 {file.split('.')[0]}")

            # Try sheet name variations (for backward compatibility)
            sheet_names = pd.ExcelFile(file).sheet_names
            expected_sheet = next((s for s in sheet_names if "AUDIT" in s.upper() and "ACTUAL" not in s.upper() and "PROJECTED" not in s.upper()), None)
            actual_sheet = next((s for s in sheet_names if "ACTUAL" in s.upper()), None)
            projected_sheet = next((s for s in sheet_names if "PROJECTED" in s.upper()), None)

            if not expected_sheet or not actual_sheet or not projected_sheet:
                st.error(f"Missing required sheets in {file}. Found: {sheet_names}")
                continue

            # Load data
            expected_df = pd.read_excel(file, sheet_name=expected_sheet)
            actual_df = pd.read_excel(file, sheet_name=actual_sheet)
            projected_df = pd.read_excel(file, sheet_name=projected_sheet)

            # Calculate actual counts per auditor
            actual_count = actual_df['Actual'].value_counts().reset_index()
            actual_count.columns = ['Name', 'Actual']

            # Merge with expected
            merged_df = expected_df[['Name', 'Expected']].merge(actual_count, on='Name', how='left')
            merged_df['Actual'] = merged_df['Actual'].fillna(0).astype(int)
            merged_df['Delta'] = (merged_df['Expected'] - merged_df['Actual']).abs()

            # Display summary table
            st.dataframe(merged_df.sort_values(by='Name').reset_index(drop=True), use_container_width=True)

            # Plot
            fig = px.bar(
                merged_df.sort_values(by='Expected', ascending=False),
                x='Name',
                y=['Expected', 'Actual'],
                barmode='group',
                title=f"Completion Comparison - {file.split('.')[0]}",
                text_auto=True,
                labels={'value': 'Count', 'Name': 'Auditor'}
            )
            fig.update_layout(xaxis_tickangle=-45, height=500, margin=dict(l=20, r=20, t=50, b=100))
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error processing {file}: {e}")
