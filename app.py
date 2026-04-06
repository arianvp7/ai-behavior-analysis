
from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "kaggle_survey_2018_multiple_choice_responses.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@st.cache_data
def load_data() -> pd.DataFrame:
    raw = pd.read_csv(DATA_FILE, low_memory=False)
    return raw.iloc[1:].copy()


st.set_page_config(page_title="Kaggle AI Behavior Analysis", layout="wide")
st.title("AI Behavior & Decision-Making Analysis")
st.caption("Built from the 2018 Kaggle Machine Learning & Data Science Survey")

if not DATA_FILE.exists():
    st.error("Dataset file is missing from the project folder.")
    st.stop()

df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Respondents", len(df))
col2.metric("Most Common Role", df["Q6"].value_counts().idxmax())
col3.metric("Top Coding Experience", df["Q24"].value_counts().idxmax())

st.subheader("Quick Findings")
st.markdown(
    """
- Real survey data from Kaggle makes this project much stronger than a fake sample dataset.
- The project focuses on roles, coding experience, tools, and work activities.
- This is a strong portfolio piece for internships involving AI, data, product, or user behavior.
"""
)

st.subheader("Role Distribution")
st.bar_chart(df["Q6"].value_counts().head(10))

st.subheader("Coding Experience")
st.bar_chart(df["Q24"].value_counts())

ide_cols = [c for c in df.columns if c.startswith("Q13_Part_")]
ide_counts = {}
for col in ide_cols:
    valid = df[col].dropna()
    if len(valid) > 0:
        ide_counts[str(valid.iloc[0])] = len(valid)
st.subheader("Top IDEs / Notebooks")
st.bar_chart(pd.Series(ide_counts).sort_values(ascending=False).head(10))

activity_cols = [c for c in df.columns if c.startswith("Q11_Part_")]
activity_counts = {}
for col in activity_cols:
    valid = df[col].dropna()
    if len(valid) > 0:
        activity_counts[str(valid.iloc[0])] = len(valid)
st.subheader("Common Work Activities")
st.bar_chart(pd.Series(activity_counts).sort_values(ascending=False).head(10))

st.subheader("Raw Data Preview")
st.dataframe(df[["Q1", "Q6", "Q24"]].head(20), use_container_width=True)
