import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel
file_path = "Herfy_QSC_Data.xlsx"
submissions_df = pd.read_excel(file_path, sheet_name="QSC field submission")
missed_df = pd.read_excel(file_path, sheet_name="QSC Missed Submission")

# Clean leader column
submissions_df['Leader'] = submissions_df['Leader_profit_Center']
missed_df['Leader'] = missed_df['Leader_profit_Center']

# Function to create summary and chart
def show_dashboard_section(title, submitted_count, missed_count):
    total = submitted_count + missed_count
    completion = (submitted_count / total * 100) if total != 0 else 0

    # Display table
    summary_df = pd.DataFrame({
        "Metric": ["Submitted", "Missed", "Total", "Completion %"],
        "Count": [submitted_count, missed_count, total, f"{completion:.2f}%"]
    })
    st.subheader(f"📊 {title}")
    st.dataframe(summary_df, hide_index=True, use_container_width=True)

    # Display chart
    fig, ax = plt.subplots()
    ax.pie([submitted_count, missed_count], labels=["Submitted", "Missed"],
           autopct='%1.1f%%', colors=["#4CAF50", "#F44336"])
    ax.set_title(f"{title} - Submission Split")
    st.pyplot(fig)

# Totals
company_submitted = len(submissions_df)
company_missed = len(missed_df)
albert_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Albert'])
albert_missed = len(missed_df[missed_df['Leader'] == 'Mr_Albert'])
said_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Said'])
said_missed = len(missed_df[missed_df['Leader'] == 'Mr_Said'])

# UI
st.title("Herfy QSC Submission Dashboard")
st.markdown("Track submission performance across managers and the company.")

show_dashboard_section("🏢 Company", company_submitted, company_missed)
show_dashboard_section("👨‍💼 Mr Albert", albert_submitted, albert_missed)
show_dashboard_section("👨‍💼 Mr Said", said_submitted, said_missed)
