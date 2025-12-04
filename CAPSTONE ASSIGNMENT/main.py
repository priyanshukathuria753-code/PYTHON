import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

# --- Configuration ---
DATA_DIR = Path('data/')
OUTPUT_DIR = Path('output/')
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / 'processing_log.txt'

# Sample column names expected in the CSV files
TIMESTAMP_COL = 'Timestamp'
KWH_COL = 'Energy_kwh'

# --- Task 3: Object-Oriented Modeling (Classes for Data Management) ---

class MeterReading:
    """Represents a single energy meter reading."""
    def __init__(self, timestamp, kwh):
        self.timestamp = pd.to_datetime(timestamp)
        self.kwh = float(kwh)

class Building:
    """Models a single campus building and its energy data."""
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
        self.df = pd.DataFrame() # DataFrame to store combined, cleaned data

    # NOTE: add_reading is primarily for conceptual OOP modeling (not used in Pandas-based analysis)
    def add_reading(self, timestamp, kwh):
        """Adds a MeterReading object."""
        self.meter_readings.append(MeterReading(timestamp, kwh))

    # FIX INCORPORATED HERE for robust column selection
    def load_data(self, df_building):
        """Loads and cleans the building's data from the combined DataFrame."""
        self.df = df_building.copy()
        
        # Select the necessary columns (TIMESTAMP_COL is now a regular column due to reset_index in Manager)
        self.df = self.df[[TIMESTAMP_COL, KWH_COL]].rename(columns={KWH_COL: 'Consumption_kwh'})
        
        # Data type conversion and validation
        self.df['Consumption_kwh'] = pd.to_numeric(self.df['Consumption_kwh'], errors='coerce')
        self.df = self.df.dropna(subset=['Consumption_kwh'])
        
        # Set the index here, right before the Building object uses it for resample/groupby
        self.df.set_index(TIMESTAMP_COL, inplace=True)
        self.df.sort_index(inplace=True)

    def calculate_total_consumption(self):
        """Calculates the total energy consumed by the building."""
        if not self.df.empty:
            return self.df['Consumption_kwh'].sum()
        return 0

    # Task 2 function
    def calculate_daily_totals(self):
        """Resamples data to daily totals."""
        # Use .resample('D') for daily totals (Task 2)
        return self.df['Consumption_kwh'].resample('D').sum().rename(f'{self.name}_Daily')

    # Task 2 function
    def calculate_weekly_aggregates(self):
        """Resamples data to weekly aggregates (mean, total)."""
        # Use .resample('W') for weekly aggregates (Task 2)
        weekly_data = self.df['Consumption_kwh'].resample('W').agg(['sum', 'mean']).rename(
            columns={'sum': f'{self.name}_Weekly_Total', 'mean': f'{self.name}_Weekly_Mean'}
        )
        return weekly_data

    # Task 2 function
    def building_wise_summary(self):
        """Generates a summary dictionary for the building."""
        if self.df.empty:
            return {'Total_kwh': 0, 'Mean_kwh': 0, 'Min_kwh': 0, 'Max_kwh': 0, 'Peak_Load_Time': 'N/A'}
        
        summary = {
            'Total_kwh': self.df['Consumption_kwh'].sum(),
            'Mean_kwh': self.df['Consumption_kwh'].mean(),
            'Min_kwh': self.df['Consumption_kwh'].min(),
            'Max_kwh': self.df['Consumption_kwh'].max()
        }
        # Find time of peak load
        peak_time = self.df['Consumption_kwh'].idxmax()
        if peak_time is not None:
             # Ensure the peak time is formatted correctly
             summary['Peak_Load_Time'] = peak_time.strftime('%Y-%m-%d %H:%M')
        else:
             summary['Peak_Load_Time'] = 'N/A'
             
        return summary

    def generate_report(self):
        """Placeholder for generating a building-specific report."""
        summary = self.building_wise_summary()
        report = f"--- Report for {self.name} ---\n"
        report += f"Total Consumption: {summary['Total_kwh']:.2f} kWh\n"
        report += f"Average Consumption: {summary['Mean_kwh']:.2f} kWh\n"
        report += f"Peak Load: {summary['Max_kwh']:.2f} kWh at {summary.get('Peak_Load_Time', 'N/A')}\n"
        return report

class BuildingManager:
    """Manages all Building objects and performs campus-wide analysis."""
    def __init__(self):
        self.buildings = {}
        self.df_combined = pd.DataFrame()
        self.daily_trends = pd.DataFrame()
        self.weekly_means = pd.DataFrame()
        self.summary_table = pd.DataFrame()
        self.log_messages = []

    # --- Task 1: Data Ingestion and Validation (FIX APPLIED HERE) ---
    def ingest_data(self):
        """
        Automatically reads multiple CSV files and combines them into one clean DataFrame.
        Handles missing files and corrupt data.
        """
        all_data = []
        csv_files = list(DATA_DIR.glob('*.csv'))

        if not csv_files:
            self.log_messages.append(f"ERROR: No CSV files found in {DATA_DIR}. Cannot proceed.")
            print(self.log_messages[-1])
            return

        for filepath in csv_files:
            building_name = filepath.stem # Use filename without extension as building name
            
            try:
                # Use on_bad_lines='skip' (replaces error_bad_lines) for corrupt data handling
                df = pd.read_csv(filepath, parse_dates=[TIMESTAMP_COL], on_bad_lines='skip', low_memory=False)
                
                # Validation: Check for essential columns
                if TIMESTAMP_COL not in df.columns or KWH_COL not in df.columns:
                    self.log_messages.append(f"WARNING: File {filepath.name} skipped. Missing '{TIMESTAMP_COL}' or '{KWH_COL}' column.")
                    continue
                
                # Add metadata (Task 1)
                df['Building'] = building_name
                all_data.append(df)
                self.log_messages.append(f"SUCCESS: Successfully read {filepath.name}.")

            except FileNotFoundError:
                # Handle exceptions: Missing files (Task 1)
                self.log_messages.append(f"ERROR: File {filepath.name} not found.")
            except Exception as e:
                self.log_messages.append(f"ERROR: An unexpected error occurred reading {filepath.name}: {e}")

        if all_data:
            # Combine all data into a single merged DataFrame
            self.df_combined = pd.concat(all_data, ignore_index=True)
            self.df_combined = self.df_combined.dropna(subset=['Building', TIMESTAMP_COL, KWH_COL])
            self.df_combined[KWH_COL] = pd.to_numeric(self.df_combined[KWH_COL], errors='coerce')
            self.df_combined = self.df_combined.dropna(subset=[KWH_COL])
            
            # CRITICAL FIX: Ensure 'Timestamp' is a regular column before grouping
            # (In case it was set as index by an earlier version or implicit operation)
            if self.df_combined.index.name == TIMESTAMP_COL:
                self.df_combined.reset_index(inplace=True)
            
            # Ensure final data is sorted by time for consistent resampling
            self.df_combined.sort_values(by=TIMESTAMP_COL, inplace=True) 

            print("Data Ingestion and Validation Complete.")
        else:
            print("No data was successfully ingested.")


    # --- Task 2: Core Aggregation Logic (Implemented within Manager/Building) ---
    def process_data(self):
        """Initializes Building objects and runs aggregation functions."""
        if self.df_combined.empty:
            return

        self.daily_trends = pd.DataFrame()
        self.weekly_means = pd.DataFrame()
        all_summaries = {}
        
        # Group by the 'Building' metadata column
        for name, group_df in self.df_combined.groupby('Building'):
            building = Building(name)
            
            # Calls load_data which now successfully selects columns and sets the index
            building.load_data(group_df) 
            self.buildings[name] = building

            # Calculate and combine daily/weekly aggregates (Task 2)
            daily = building.calculate_daily_totals()
            weekly = building.calculate_weekly_aggregates()
            
            self.daily_trends = pd.merge(self.daily_trends, daily, left_index=True, right_index=True, how='outer')
            self.weekly_means = pd.merge(self.weekly_means, weekly[f'{name}_Weekly_Mean'], left_index=True, right_index=True, how='outer')
            
            # Store results in Dictionaries for building summaries (Task 2)
            all_summaries[name] = building.building_wise_summary()

        # Convert summaries to a DataFrame
        self.summary_table = pd.DataFrame.from_dict(all_summaries, orient='index')
        print("Data Processing and Aggregation Complete.")


    # --- Task 4: Visual Output with Matplotlib ---
    def generate_visual_dashboard(self):
        """Generates multiple plots in a dashboard-style layout."""
        if self.daily_trends.empty or self.weekly_means.empty or self.df_combined.empty:
            self.log_messages.append("ERROR: Cannot generate visuals. Aggregated data is missing.")
            print(self.log_messages[-1])
            return

        # Use plt.subplots() to create a unified figure (Task 4)
        fig, axes = plt.subplots(3, 1, figsize=(14, 18))
        fig.suptitle('Campus Energy Consumption Dashboard', fontsize=20, y=1.02)
        
        # 1. Trend Line – daily consumption over time for all buildings (Task 4)
        self.daily_trends.plot(ax=axes[0], kind='line')
        axes[0].set_title('Daily Total Consumption Trend Over Time')
        axes[0].set_ylabel('Total Consumption (kWh)')
        axes[0].legend(title='Building')
        axes[0].grid(True, linestyle='--', alpha=0.6)

        # 2. Bar Chart – compare average weekly usage across buildings (Task 4)
        avg_weekly_usage = self.weekly_means.mean(skipna=True).sort_values(ascending=False)
        # Clean index for display
        avg_weekly_usage.index = [idx.replace('_Weekly_Mean', '') for idx in avg_weekly_usage.index] 
        
        avg_weekly_usage.plot(ax=axes[1], kind='bar')
        axes[1].set_title('Average Weekly Consumption per Building')
        axes[1].set_ylabel('Average Weekly Usage (kWh)')
        axes[1].set_xlabel('Building Name')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].grid(axis='y', linestyle='--', alpha=0.6)

        # 3. Scatter Plot – plot peak-hour consumption vs. time/building (Task 4)
        # Resample to a frequent interval (e.g., hourly) to plot peak events
        peak_consumption = self.df_combined.set_index(TIMESTAMP_COL)[KWH_COL].resample('H').max().dropna()
        
        axes[2].scatter(peak_consumption.index, peak_consumption.values, alpha=0.7, s=50, c='red')
        axes[2].set_title('Hourly Peak Consumption Events (Scatter Plot)')
        axes[2].set_ylabel('Peak Consumption (kWh)')
        axes[2].set_xlabel('Time')
        axes[2].grid(True, linestyle='--', alpha=0.6)

        # Save the chart as dashboard.png (Task 4)
        plt.tight_layout(rect=[0, 0, 1, 0.98])
        dashboard_path = OUTPUT_DIR / 'dashboard.png'
        plt.savefig(dashboard_path)
        plt.close(fig)
        print(f"Visual dashboard saved to {dashboard_path}.")


    # --- Task 5: Persistence and Executive Summary ---
    def generate_reports(self):
        """Exports data and creates the written summary report."""
        
        # 1. Export Final processed dataset (Task 5)
        if not self.df_combined.empty:
            cleaned_path = OUTPUT_DIR / 'cleaned_energy_data.csv'
            # Reset index before export to save 'Timestamp' as a column
            self.df_combined.reset_index(drop=True).to_csv(cleaned_path, index=False)
            print(f"Cleaned energy data exported to {cleaned_path}.")
        
        # 2. Export Summary stats (Task 5)
        if not self.summary_table.empty:
            summary_path = OUTPUT_DIR / 'building_summary.csv'
            self.summary_table.to_csv(summary_path)
            print(f"Building summary exported to {summary_path}.")
            
        # 3. Create a short summary report (summary.txt) (Task 5)
        summary_txt_path = OUTPUT_DIR / 'summary.txt'
        
        # Calculate key metrics for the summary
        total_campus_consumption = self.summary_table['Total_kwh'].sum()
        highest_consuming_building = self.summary_table['Total_kwh'].idxmax()
        highest_consumption = self.summary_table['Total_kwh'].max()
        
        # Find absolute peak load time from the combined data
        if not self.df_combined.empty:
            peak_load_value_idx = self.df_combined[KWH_COL].idxmax()
            peak_load_time = self.df_combined.loc[peak_load_value_idx, TIMESTAMP_COL].strftime('%Y-%m-%d %H:%M')
            peak_load_value = self.df_combined.loc[peak_load_value_idx, KWH_COL]
        else:
             peak_load_time = 'N/A'
             peak_load_value = 0

        # Trends
        daily_total_consumption = self.daily_trends.sum(axis=1)
        if daily_total_consumption.shape[0] > 1:
            daily_growth_rate = daily_total_consumption.pct_change().mean() * 100
        else:
            daily_growth_rate = 0.0

        trend_statement = "Campus-wide daily consumption shows an average growth of" if daily_growth_rate > 0 else "Campus-wide daily consumption shows an average change of"
        
        summary_report = "--- Executive Energy Summary Report ---\n\n"
        summary_report += f"1. Total Campus Consumption: {total_campus_consumption:.2f} kWh\n"
        summary_report += f"2. Highest-Consuming Building: **{highest_consuming_building}** ({highest_consumption:.2f} kWh)\n"
        summary_report += f"3. Peak Load Event: **{peak_load_value:.2f} kWh** occurred at {peak_load_time}\n"
        summary_report += f"4. Weekly/Daily Trends: {trend_statement} **{abs(daily_growth_rate):.2f}%**.\n"
        summary_report += "---------------------------------------\n\n"
        summary_report += "Detailed Building Summaries (mean, min, max, total):\n"
        summary_report += self.summary_table.to_string(float_format='%.2f')
        
        with open(summary_txt_path, 'w') as f:
            f.write(summary_report)
            
        # Print summary to console (Task 5)
        print("\n" + summary_report)
        print(f"Executive summary saved to {summary_txt_path}.")
        
        # Log any issues encountered during Task 1 (Task 1)
        with open(LOG_FILE, 'w') as f:
            f.write("--- Data Processing Log ---\n")
            f.write("\n".join(self.log_messages))
        print(f"Processing log saved to {LOG_FILE}.")

# --- Main Execution Block ---

def main():
    manager = BuildingManager()

    print("--- Starting Task 1: Data Ingestion and Validation ---")
    manager.ingest_data()
    print("-" * 50)

    if not manager.df_combined.empty:
        print("--- Starting Task 2 & 3: Core Aggregation and OOP Modeling ---")
        manager.process_data()
        print("-" * 50)

        print("--- Starting Task 4: Visual Output with Matplotlib ---")
        manager.generate_visual_dashboard()
        print("-" * 50)

        print("--- Starting Task 5: Persistence and Executive Summary ---")
        manager.generate_reports()
        print("-" * 50)
    else:
        print("Script terminated due to failure in Task 1 (No data ingested).")

if __name__ == "__main__":
    main()