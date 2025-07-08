import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel file and read both sheets
file_path = "Herfy_QSC_Data.xlsx"
submissions_df = pd.read_excel(file_path, sheet_name="QSC field submissions")
missed_df = pd.read_excel(file_path, sheet_name="QSC missed submission")

# Standardize leader column
submissions_df['Leader'] = submissions_df['Leader_profit_Center']
missed_df['Leader'] = missed_df['Leader_profit_Center']

# Define function to plot pie chart
def plot_completion_chart(submitted, missed, title):
    total = submitted + missed
    values = [submitted, missed]
    labels = ['Submitted', 'Missed']
    colors = ['#4CAF50', '#F44336']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct=lambda p: f'{p:.1f}%\n({int(p * total / 100)})', colors=colors)
    ax.set_title(title)
    st.pyplot(fig)

# Count company-wide totals (ignore nulls in Leader)
company_submitted = len(submissions_df)
company_missed = len(missed_df)

# Count for Mr_Albert
albert_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Albert'])
albert_missed = len(missed_df[missed_df['Leader'] == 'Mr_Albert'])

# Count for Mr_Said
said_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Said'])
said_missed = len(missed_df[missed_df['Leader'] == 'Mr_Said'])

# Streamlit app
st.title("Herfy QSC Submission Dashboard")

st.subheader("🍽️ Overall Company Submission Completion")
plot_completion_chart(company_submitted, company_missed, "Company Completion")

st.subheader("👨‍💼 Mr Albert's Submission Completion")
plot_completion_chart(albert_submitted, albert_missed, "Mr Albert")

st.subheader("👨‍💼 Mr Said's Submission Completion")
plot_completion_chart(said_submitted, said_missed, "Mr Said")
