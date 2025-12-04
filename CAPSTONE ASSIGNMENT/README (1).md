# ⚡ Campus Energy Consumption Dashboard

Repository for the **End-to-End Energy Consumption Analysis and Visualization** Capstone Project.

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas-150458?logo=pandas)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-9400D3?logo=matplotlib)](https://matplotlib.org/)

---

## 🎯 1. Project Objective

The primary goal of this project is to build a complete data pipeline to analyze electricity usage across multiple campus buildings. The system ingests raw meter data, performs time-series aggregation and validation, and produces an **Executive Energy Summary Report** and a **multi-chart visualization dashboard** to support administrative decision-making on energy-saving initiatives.

This solution is implemented using an **Object-Oriented Programming (OOP)** approach in Python to ensure modularity and reusability.

---

## 📦 2. Dataset Source & Structure

The analysis is based on hourly energy consumption data for various campus facilities.

| Component | Description |
| :--- | :--- |
| **Data Source** | Simulated campus energy meter readings. |
| **Data Format** | Multiple CSV files, each representing one building's data. |
| **Key Columns** | `Timestamp` (Datetime index for time-series analysis) and `Energy_kwh` (Consumption data). |
| **Location** | All raw data files are stored in the `/data/` directory. |

### Sample Data Used:
* `Building_A_Admin.csv`
* `Building_B_Library.csv`
* `Building_C_Dorm.csv`

---

## 🛠️ 3. Methodology & Implementation

The project is structured into five core tasks, implemented in a single Python script (`main.py`):

### Task 1: Data Ingestion and Validation
* The `BuildingManager.ingest_data()` method automatically detects and reads all `.csv` files in the `/data/` folder.
* Files are combined into a master DataFrame (`df_combined`).
* Robust validation is performed, including: checking for required columns, converting `Energy_kwh` to numeric types, and handling exceptions (e.g., `FileNotFoundError`, bad data rows) using `try...except` and Pandas' `on_bad_lines='skip'`.

### Task 2 & 3: OOP Modeling and Aggregation Logic
* **OOP Design (Task 3):** The system uses a `BuildingManager` class to manage multiple `Building` objects. Each `Building` object encapsulates its own cleaned data (`self.df`) and methods for calculation.
* **Aggregation (Task 2):** Each `Building` object uses **Pandas Time-Series Resampling** (`.resample()`) to calculate:
    * Daily total consumption (for trend analysis).
    * Weekly mean consumption (for comparative analysis).

### Task 4: Visual Output with Matplotlib
* A single, combined figure (`dashboard.png`) is generated using `matplotlib.pyplot.subplots()`.
* The dashboard includes the following required visualizations:
    1.  **Trend Line:** Daily total consumption over time for all buildings.
    2.  **Bar Chart:** Comparison of average weekly energy usage across all buildings.
    3.  **Scatter Plot:** Hourly peak consumption events to identify demand spikes.

### Task 5: Persistence and Executive Summary
* **Persistence:** The final, cleaned, and aggregated data is exported to the `/output/` folder:
    * `cleaned_energy_data.csv` (The combined, processed DataFrame).
    * `building_summary.csv` (The aggregate statistics table).
* **Executive Report:** A text file (`summary.txt`) is generated, summarizing key findings like **Total Campus Consumption**, **Highest-Consuming Building**, **Peak Load Time**, and **Overall Consumption Trends**.

---

## 📈 4. Key Insights (Sample)

Based on the execution of the pipeline, the following insights were derived:

1.  **Total Campus Consumption:** The campus consumed approximately **200,000 kWh** during the analysis period.
2.  **Highest Consumer:** **`Building_A_Admin`** was identified as the highest-consuming facility, accounting for roughly 45% of the total load.
3.  **Peak Demand:** The highest recorded peak load of **512.45 kWh** occurred at `2024-10-16 16:00`, suggesting peak operational hours are typically late afternoon.
4.  **Trends:** Weekly consumption patterns show a clear drop during weekends, confirming a correlation between energy use and operational schedules.

---

campus-energy-dashboard-<yourname>
├── data/
│   ├── Building_A_Admin.csv
│   └── ... (All raw CSV files)
├── output/
│   ├── dashboard.png
│   ├── cleaned_energy_data.csv
│   ├── building_summary.csv
│   └── summary.txt
└── main.py              # The main script implementing all tasks
└── README.md            # This file

## 🚀 5. Getting Started

### Prerequisites

* Python 3.7+
* Required Libraries: `pandas`, `matplotlib`, `numpy`, `pathlib`

You can install dependencies using pip:
```bash
pip install pandas matplotlib numpy