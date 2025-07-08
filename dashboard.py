import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ------------------ Page Config ------------------
st.set_page_config(page_title="Herfy QSC Dashboard", layout="centered")

# ------------------ Branding Header ------------------
st.markdown("""
<h2 style='text-align: center; color: #6A5ACD;'>Herfy QSC Submission Dashboard</h2>
<p style='text-align: center; color: gray;'>Powered by Taqtics</p>
""", unsafe_allow_html=True)

# ------------------ Load Data ------------------
file_path = "Herfy_QSC_Data.xlsx"
submissions_df = pd.read_excel(file_path, sheet_name="QSC field submission")
missed_df = pd.read_excel(file_path, sheet_name="QSC Missed Submission")

# Standardize leader column
submissions_df['Leader'] = submissions_df['Leader_profit_Center']
missed_df['Leader'] = missed_df['Leader_profit_Center']

# ------------------ Helper Function ------------------
def show_section(title, submitted, missed):
    total = submitted + missed
    completion = (submitted / total * 100) if total else 0

    # Summary Table
    st.markdown(f"### {title}")
    st.dataframe(pd.DataFrame({
        "Metric": ["Submitted", "Missed", "Total", "Completion %"],
        "Value": [submitted, missed, total, f"{completion:.2f}%"]
    }), use_container_width=True, hide_index=True)

    # Pie Chart
    fig = go.Figure(data=[go.Pie(
        labels=["Submitted", "Missed"],
        values=[submitted, missed],
        marker=dict(colors=["#2ecc71", "#e74c3c"]),
        hole=0.4,
        textinfo='label+percent'
    )])
    fig.update_layout(height=350, showlegend=True, title=f"{title} - Submission Split")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ Count Logic ------------------
company_submitted = len(submissions_df)
company_missed = len(missed_df)

albert_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Albert'])
albert_missed = len(missed_df[missed_df['Leader'] == 'Mr_Albert'])

said_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Said'])
said_missed = len(missed_df[missed_df['Leader'] == 'Mr_Said'])

# ------------------ Sections ------------------
show_section("🏢 Company Summary", company_submitted, company_missed)
show_section("👨‍💼 Mr Albert", albert_submitted, albert_missed)
show_section("👨‍💼 Mr Said", said_submitted, said_missed)
