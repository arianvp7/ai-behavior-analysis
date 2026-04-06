
from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "kaggle_survey_2018_multiple_choice_responses.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_FILE, low_memory=False)
    question_row = raw.iloc[0]
    df = raw.iloc[1:].copy()
    return df, question_row


def add_chart_title(ax, title: str, xlabel: str = "", ylabel: str = "") -> None:
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def save_top_roles(df: pd.DataFrame) -> None:
    role_counts = df["Q6"].value_counts().head(10)
    ax = role_counts.plot(kind="bar", figsize=(10, 5))
    add_chart_title(ax, "Top Roles in the 2018 Kaggle ML/DS Survey", "", "Number of respondents")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_top_roles.png", dpi=200)
    plt.close()


def save_coding_experience(df: pd.DataFrame) -> None:
    order = [
        "< 1 year",
        "1-2 years",
        "3-5 years",
        "5-10 years",
        "10-20 years",
        "20-30 years",
        "30-40 years",
        "40+ years",
        "I have never written code but I want to learn",
        "I have never written code and I do not want to learn",
    ]
    counts = df["Q24"].value_counts()
    counts = counts.reindex([x for x in order if x in counts.index]).dropna()
    ax = counts.plot(kind="bar", figsize=(10, 5))
    add_chart_title(ax, "Coding Experience Distribution", "", "Number of respondents")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_coding_experience.png", dpi=200)
    plt.close()


def save_ide_usage(df: pd.DataFrame) -> None:
    ide_cols = [c for c in df.columns if c.startswith("Q13_Part_")]
    ide_counts = {}
    for col in ide_cols:
        valid = df[col].dropna()
        if len(valid) > 0:
            label = str(valid.iloc[0]) if str(valid.iloc[0]) != "-1" else col
            # better label from the question row isn't available here; use observed non-null value
            ide_counts[label] = len(valid)
    ide_series = pd.Series(ide_counts).sort_values(ascending=False).head(10)
    ax = ide_series.plot(kind="bar", figsize=(11, 5))
    add_chart_title(ax, "Most Used IDEs / Notebooks", "", "Selections")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_ide_usage.png", dpi=200)
    plt.close()


def save_activity_usage(df: pd.DataFrame) -> None:
    activity_cols = [c for c in df.columns if c.startswith("Q11_Part_")]
    activity_counts = {}
    for col in activity_cols:
        valid = df[col].dropna()
        if len(valid) > 0:
            label = str(valid.iloc[0]) if str(valid.iloc[0]) != "-1" else col
            activity_counts[label] = len(valid)
    activity_series = pd.Series(activity_counts).sort_values(ascending=False).head(10)
    ax = activity_series.plot(kind="bar", figsize=(12, 6))
    add_chart_title(ax, "Common Work Activities in Data Roles", "", "Selections")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "04_work_activities.png", dpi=200)
    plt.close()


def write_summary(df: pd.DataFrame) -> None:
    total = len(df)
    top_role = df["Q6"].value_counts().idxmax()
    top_role_count = int(df["Q6"].value_counts().max())
    top_exp = df["Q24"].value_counts().idxmax()
    top_exp_count = int(df["Q24"].value_counts().max())

    ide_cols = [c for c in df.columns if c.startswith("Q13_Part_")]
    ide_counts = {}
    for col in ide_cols:
        valid = df[col].dropna()
        if len(valid) > 0:
            ide_counts[str(valid.iloc[0])] = len(valid)
    top_ide = max(ide_counts, key=ide_counts.get)

    text = f"""Kaggle 2018 Survey Analysis Summary
================================

Rows analyzed: {total}
Most common role: {top_role} ({top_role_count})
Most common coding-experience level: {top_exp} ({top_exp_count})
Most frequently used IDE / notebook: {top_ide} ({ide_counts[top_ide]})

Suggested talking points:
- The dataset shows a broad mix of roles, but data scientists and related roles are highly represented.
- Many respondents fall in the early-to-mid coding experience range, showing the field includes many developing practitioners.
- Jupyter-style notebook workflows appear prominently, highlighting the importance of exploratory and interactive tooling.
- Real-world survey data lets you discuss behavior, tools, and workflow patterns instead of relying on fake sample data.
"""
    (OUTPUT_DIR / "summary_report.txt").write_text(text, encoding="utf-8")
    print(text)
    print(f"Saved charts and summary to: {OUTPUT_DIR}")


def main() -> None:
    if not DATA_FILE.exists():
        print(f"Missing data file: {DATA_FILE.name}")
        return
    df, _ = load_data()
    save_top_roles(df)
    save_coding_experience(df)
    save_ide_usage(df)
    save_activity_usage(df)
    write_summary(df)


if __name__ == "__main__":
    main()
