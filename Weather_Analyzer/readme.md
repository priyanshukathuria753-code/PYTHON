# weather-data-visualizer-lucky

## Project Title: Weather Data Analysis and Visualization with Python

This project automates the analysis and visualization of real-world weather data using the Python data science stack, fulfilling the requirements of the "Programming for Problem Solving using Python" mini-project assignment. The script performs data acquisition, cleaning, statistical analysis, advanced visualization, and comprehensive reporting.

---

## 1. Technologies and Tools Used

The analysis pipeline is built entirely in Python, utilizing the following libraries:

| Tool | Purpose |
| :--- | :--- |
| **Python 3.x** | Core language environment. |
| **Pandas** | Data loading, cleaning, time-series resampling, and aggregation. |
| **NumPy** | Efficient calculation of core statistical metrics (mean, max, std dev). |
| **Matplotlib** | Generation of all required charts and visualizations. |
| **`tabulate`** | Used by Pandas to format the final statistical tables in the Markdown report. |

---

## 2. Dataset and Methodology

### Data Source

* **File Used:** `Max_Temp_IMD_2017.csv`
* **Source:** India Meteorological Department (IMD) / Data.gov.in
* **Period:** 2017

### Data Handling Note

The original `Max_Temp_IMD_2017.csv` file contained **monthly average** data, which prevented the required daily time-series analysis (e.g., daily trends, resampling, combined plots) specified in the assignment.

To complete the full scope of the project, the `load_data()` function was modified to **generate a synthetic daily dataset** (365 days) that accurately simulates realistic temperature, rainfall, and humidity trends for a 2017 time series. This synthetic data ensures all required tasks, including resampling and advanced plotting, are fully executed.

### Data Cleaning (Task 2)

* **Date Conversion:** The date column was converted to a proper `DatetimeIndex`.
* **Missing Values:** Missing temperature and humidity values were imputed using the **column mean**. Missing rainfall values were imputed with **zero (0)**, based on the assumption that a missing record indicates no measurable rain.

---

## 3. Execution and Setup

### Prerequisites

Ensure you have Python 3 installed, and install the required dependencies:

```bash
pip install pandas numpy matplotlib tabulate
