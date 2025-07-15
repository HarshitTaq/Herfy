import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📋 Auditor Completion Dashboard")

uploaded_files = st.file_uploader("Upload Multiple Audit Excel Files", type="xlsx", accept_multiple_files=True)

def process_audit(file):
    # Try to extract base name for display (e.g., CLEANLINESS)
    base_name = file.name.split('.')[0].replace("_", " ").title()

    try:
        xls = pd.ExcelFile(file)
        # Detect sheets dynamically
        sheets = xls.sheet_names

        # Extract matching sheet names
        audit_sheet = [s for s in sheets if "AUDIT" in s.upper() and "ACTUAL" not in s.upper() and "PROJECTED" not in s.upper()]
        actual_sheet = [s for s in sheets if "ACTUAL" in s.upper()]
        projected_sheet = [s for s in sheets if "PROJECTED" in s.upper()]

        if not (audit_sheet and actual_sheet and projected_sheet):
            st.warning(f"❌ Skipping {file.name} — required sheets missing.")
            return

        audit_df = pd.read_excel(xls, sheet_name=audit_sheet[0])
        actual_df = pd.read_excel(xls, sheet_name=actual_sheet[0])
        projected_df = pd.read_excel(xls, sheet_name=projected_sheet[0])

        # Clean names
        audit_df['Name'] = audit_df['Name'].astype(str).str.strip()
        actual_df['Actual'] = actual_df['Actual'].astype(str).str.strip()
        projected_df['Projected'] = projected_df['Projected'].astype(str).str.strip()

        # Expected count
        expected = projected_df['Projected'].value_counts().reset_index()
        expected.columns = ['Name', 'Expected']

        # Actual count
        actual = actual_df['Actual'].value_counts().reset_index()
        actual.columns = ['Name', 'Actual']

        # Merge
        summary = pd.merge(expected, actual, on='Name', how='outer').fillna(0)
        summary['Expected'] = summary['Expected'].astype(int)
        summary['Actual'] = summary['Actual'].astype(int)
        summary['Delta'] = (summary['Expected'] - summary['Actual']).abs()

        # Display
        st.subheader(f"📊 {base_name} Completion Summary")
        st.dataframe(summary.sort_values("Name"))

        fig = px.bar(summary.sort_values("Expected", ascending=False),
                     x='Name', y=['Expected', 'Actual'],
                     barmode='group',
                     title=f"{base_name} - Expected vs Actual Submissions",
                     labels={'value': 'Count', 'Name': 'Auditor'})
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing {f
