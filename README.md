# ai-behavior-analysis
Python project analyzing real Kaggle survey data to study AI usage, roles, and behavioral patterns.

# AI Behavior & Decision-Making Analysis

Understanding how AI changes human behavior — not just productivity.

## 📊 Sample Results

![Roles](outputs/01_top_roles.png)
![Experience](outputs/02_coding_experience.png)
![IDE Usage](outputs/03_ide_usage.png)
![Work Activities](outputs/04_work_activities.png)

## Overview
This project analyzes real-world data from the Kaggle Machine Learning & Data Science Survey (2018) to understand AI usage, roles, coding experience, and workflow behavior.

## Key Findings
- Students and early-career users make up a large portion of the field  
- Most respondents fall in the 1–2 year coding experience range  
- Jupyter-style tools dominate workflows  
- Real-world survey data reveals how tools and roles shape behavior  

## Tools Used
- Python  
- pandas  
- matplotlib  
- streamlit  

## How to Run
```bash
python3 -m pip install -r requirements.txt
python3 analysis.py
python3 -m streamlit run app.py
