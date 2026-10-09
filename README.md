F1-Strategy-analysis-
Initial focus on data science and visualization tools

🏎️ 2026 F1 Command Center — Strategy & Telemetry Dashboard

An interactive Formula 1 strategy dashboard built with **Streamlit** and **Python**, designed to analyze driver pace, tyre wear, circuit speed profiles, and race strategy across the **2026 F1 Season** (up to the Bahrain Grand Prix in Malaysia).

The application focuses on an in-depth constructor comparison between **Mercedes** and **Ferrari** ).

---

📌 Features

 📊 Tab 1: Race Strategy Overview
* **Top 5 Pace Distribution:** Box plot analysis visualizing lap time consistency and variance among top finishers.
* **Tyre Wear Trendlines:** Linear regression modeling via `scikit-learn` to calculate degradation rates ($\text{sec/lap}$) over stint lengths.
* **Track Layout:** High-resolution circuit visualization loaded locally from custom media storage.

🏎️ Tab 2: Constructor Deep-Dive (4-Driver Analysis)
* **Sector-Wise Speed Profiling:** Dynamic speed curves mapping velocity across Sectors 1, 2, and 3 based on track characteristics (e.g., high-speed Monza vs street circuit Monaco).
* **Tyre Degradation Regression:** Stint-by-stint comparative tyre wear model across all four Mercedes and Ferrari drivers.
* **Track Evolution Tracking:** Monitors grip improvement and lap time evolution over full race distances.
* **Lap-by-Lap Teammate Duel:** Real-time pace comparison tracing gap deltas and stint progression between teammates.
* **Dynamic DNF Logic:** Truncates telemetry and lap-by-lap data at exact retirement laps (e.g., George Russell's PU failure on Lap 50 at the Bahrain GP in Malaysia).

---

 🛠️ Tech Stack & Dependencies

* **Frontend & Framework:** Streamlit
* **Data Processing:** `pandas`, `numpy`
* **Machine Learning & Modeling:** `scikit-learn` (`LinearRegression`)
* **Data Visualization:** `matplotlib` (Pit-wall dark theme)


  🚀 Getting Started
  
1. Clone & Set Up Workspace

Bash:
cd f1_dashboard
python -m venv .venv
Activate Virtual Environment:

Windows: .venv\Scripts\activate

Mac/Linux: source .venv/bin/activate

2. Install Dependencies

Bash:
pip install -r requirements.txt

3. Run Application

Bash:
streamlit run app.py
