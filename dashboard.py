import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.title("📋 Auditor Completion Dashboard")

DATA_DIR = "data"  # folder containing all your Excel files

def process_audit(filepath):
    base_name = os.path.splitext(os.path.basename(filepath))[0].replace("_", " ").title()

    try:
        xls = pd.ExcelFile(filepath)
        sheets = xls.sheet_names

        audit_sheet = [s for s in sheets if "AUDIT" in s.upper() and "ACTUAL" not in s.upper() and "PROJECTED" not in s.upper()]
        actual_sheet = [s for s in sheets if "ACTUAL" in s.upper()]
        projected_sheet = [s for s in sheets if "PROJECTED" in s.upper()]

        if not (audit_sheet and actual_sheet and projected_sheet):
            st.warning(f"❌ Skipping {filepath} — required sheets missing.")
            return

        audit_df = pd.read_excel(xls, sheet_name=audit_sheet[0])
        actual_df = pd.read_excel(xls, sheet_name=actual_sheet[0])
        projected_df = pd.read_excel(xls, sheet_name=projected_sheet[0])

        # Normalize names
        audit_df['Name'] = audit_df['Name'].astype(str).str.strip()
        actual_df['Actual'] = actual_df['Actual'].astype(str).str.strip()
        projected_df['Projected'] = projected_df['Projected'].astype(str).str.strip()

        # Count expected per auditor
        expected = projected_df['Projected'].value_counts().reset_index()
        expected.columns = ['Name', 'Expected']

        # Count actual per auditor
        actual = actual_df['Actual'].value_counts().reset_index()
        actual.columns = ['Name', 'Actual']

        # Merge summary
        summary = pd.merge(expected, actual, on='Name', how='outer').fillna(0)
        summary['Expected'] = summary['Expected'].astype(int)
        summary['Actual'] = summary['Actual'].astype(int)
        summary['Delta'] = (summary['Expected'] - summary['Actual']).abs()

        # Display table
        st.subheader(f"📊 {base_name} Completion Summary")
        st.dataframe(summary.sort_values("Name"))

        # Plot
        fig = px.bar(summary.sort_values("Expected", ascending=False),
                     x='Name', y=['Expected', 'Actual'],
                     barmode='group',
                     title=f"{base_name} - Expected vs Actual Submissions",
                     labels={'value': 'Count', 'Name': 'Auditor'})
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing {filepath}: {str(e)}")

# Run for all Excel files in /data
excel_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]

if not excel_files:
    st.warning("📂 No Excel files found in the 'data/' folder. Add your audit files there.")
else:
    for file in excel_files:
        process_audit(file)
