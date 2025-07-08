import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Herfy QSC Dashboards", layout="centered")

# ------------------ Branding Header ------------------
st.markdown("""
<h2 style='text-align: center; color: #6A5ACD;'>Herfy QSC Submission + Ideal Store Dashboard</h2>
<p style='text-align: center; color: gray;'>Powered by Taqtics</p>
""", unsafe_allow_html=True)

# ------------------ Helper Function ------------------
def show_section(title, submitted, missed, color=["#2ecc71", "#e74c3c"]):
    total = submitted + missed
    completion = (submitted / total * 100) if total else 0

    st.markdown(f"### {title}")
    st.dataframe(pd.DataFrame({
        "Metric": ["Submitted", "Missed", "Total", "Completion %"],
        "Value": [submitted, missed, total, f"{completion:.2f}%"]
    }), use_container_width=True, hide_index=True)

    fig = go.Figure(data=[go.Pie(
        labels=["Submitted"] if missed == 0 else ["Submitted", "Missed"],
        values=[submitted] if missed == 0 else [submitted, missed],
        marker=dict(colors=color),
        hole=0.4,
        textinfo='label+percent'
    )])
    fig.update_layout(height=350, showlegend=True, title=f"{title} - Submission Split")
    st.plotly_chart(fig, use_container_width=True)

# ------------------ Section 1: QSC Submission ------------------

file_qsc = "Herfy_QSC_Data.xlsx"
submissions_df = pd.read_excel(file_qsc, sheet_name="QSC field submission")
missed_df = pd.read_excel(file_qsc, sheet_name="QSC Missed Submission")

submissions_df['Leader'] = submissions_df['Leader_profit_Center']
missed_df['Leader'] = missed_df['Leader_profit_Center']

st.markdown("## 📊 QSC Submission Process")

company_submitted = len(submissions_df)
company_missed = len(missed_df)

albert_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Albert'])
albert_missed = len(missed_df[missed_df['Leader'] == 'Mr_Albert'])

said_submitted = len(submissions_df[submissions_df['Leader'] == 'Mr_Said'])
said_missed = len(missed_df[missed_df['Leader'] == 'Mr_Said'])

show_section("🏢 Company Summary (QSC)", company_submitted, company_missed)
show_section("👨‍💼 Mr Albert (QSC)", albert_submitted, albert_missed)
show_section("👨‍💼 Mr Said (QSC)", said_submitted, said_missed)

# ------------------ Section 2: Ideal Store ------------------

file_ideal = "Herfy_QSC_IDEAL_STORE.xlsx"
ideal_df = pd.read_excel(file_ideal)

ideal_df['Director'] = ideal_df["Director of Operation's Name:"]
ideal_df = ideal_df.dropna(subset=['Director'])

st.markdown("---")
st.markdown("## 🏬 Ideal Store Process")

company_ideal = len(ideal_df)
said_ideal = len(ideal_df[ideal_df['Director'] == 'Mr.said Ouafik'])
albert_ideal = len(ideal_df[ideal_df['Director'] == 'Mr Albert Russell'])

show_section("🏢 Company Summary (Ideal Store)", company_ideal, 0)
show_section("👨‍💼 Mr Albert Russell (Ideal Store)", albert_ideal, 0)
show_section("👨‍💼 Mr Said Ouafik (Ideal Store)", said_ideal, 0)
