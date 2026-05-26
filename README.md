# Agentic Workflow Impact Model 
**Author:** Dhruv Jani 

## Overview
A Python-based quantitative pipeline that uses **Event Study Methodology** and **Ordinary Least Squares (OLS) regression** to measure the financial impact of corporate AI announcements. By isolating specific product rollouts from broader market movements (NASDAQ), this tool helps investors determine if an AI integration actually drives valuation.

## Key Findings (Top Performers)
* **monday.com (MNDY) | +8.51% CAR:** Strong market validation for "Monday AI" as a core revenue and retention driver.
* **Adobe (ADBE) | +3.03% CAR:** Firefly AI rewarded as a highly effective protective moat for its creative monopoly.
* **Box (BOX) | +0.41% CAR:** Muted reaction; the market priced in "Box AI" as standard table stakes rather than a revolutionary driver.

## Tech Stack
* **Data & Math:** `pandas`, `yfinance` (Yahoo Finance API), `statsmodels`
* **Visualization:** `matplotlib`, `streamlit` (Web App), `plotly`

## Quick Start
Run these commands in your terminal to execute the entire pipeline from scratch and launch the interactive portfolio dashboard.

**1. Setup Environment**
```
git clone https://github.com/optimizedlp/Agentic-Workflow-Impact-Model.git
cd Agentic-Workflow-Impact-Model
python -m venv venv
pip install -r requirements.txt
```

**2. Execute Quantitative Engine**
# Fetches API data, runs regressions, and generates memos in /output
```
python src/report_writer.py
```

**3. Launch Interactive Dashboard**
# Aggregates the memos and spins up a local web app
```
python src/aggregator.py
streamlit run app.py
```