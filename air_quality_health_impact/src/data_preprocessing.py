# src/data_preprocessing.py
import pandas as pd
import numpy as np
from src.utils import load_data, save_data, check_missing_values

def generate_synthetic_data(num_days=365):
    """Generates synthetic air quality and health data."""
    dates = pd.date_range("2023-01-01", periods=num_days, freq="D")
    # Simulate air quality data (PM2.5, NO2, O3) - adding some seasonality
    pm25 = 20 + 15 * np.sin(2 * np.pi * np.arange(num_days) / 365) + 5 * np.random.randn(num_days)
    no2 = 30 + 10 * np.cos(2 * np.pi * np.arange(num_days) / 365) + 3 * np.random.randn(num_days)
    o3 = 40 + 20 * np.sin(2 * np.pi * np.arange(num_days) / 365 + np.pi/2) + 8 * np.random.randn(num_days)

    #Ensure that values are not less than 0
    pm25 = np.maximum(pm25, 0)
    no2 = np.maximum(no2, 0)
    o3 = np.maximum(o3, 0)
    air_quality_df = pd.DataFrame({"date": dates, "PM2.5": pm25, "NO2": no2, "O3": o3})

    # Simulate health data (hospital admissions, asthma rates) - correlated with pollution
    hospital_admissions = 50 + 0.5 * pm25 + 0.2 * no2 + 2 * np.random.randn(num_days)
    asthma_rate = 5 + 0.1 * pm25 + 0.05 * o3 + 0.5 * np.random.randn(num_days)

    #Ensure the values are not less than 0
    hospital_admissions = np.maximum(hospital_admissions, 0).astype(int)  #Admissions should be integers
    asthma_rate = np.maximum(asthma_rate, 0)
    health_df = pd.DataFrame({"date": dates, "hospital_admissions": hospital_admissions, "asthma_rate": asthma_rate})

    return air_quality_df, health_df


def clean_data(air_quality_df, health_df):
    """Cleans and prepares the data for analysis."""

    # Convert 'date' columns to datetime objects
    air_quality_df['date'] = pd.to_datetime(air_quality_df['date'])
    health_df['date'] = pd.to_datetime(health_df['date'])

    # Check for missing values
    check_missing_values(air_quality_df)
    check_missing_values(health_df)

    # Handle missing values (if any) - simple imputation for this example
    # In a real project, you'd investigate *why* data is missing.
    air_quality_df.fillna(air_quality_df.mean(numeric_only=True), inplace=True)
    health_df.fillna(health_df.mean(numeric_only=True), inplace=True)

    # Merge the dataframes
    combined_df = pd.merge(air_quality_df, health_df, on="date", how="inner")

    return combined_df



def main():
     # Generate and save synthetic data
    air_quality_df, health_df = generate_synthetic_data()
    save_data(air_quality_df, "data/raw/air_quality.csv")
    save_data(health_df, "data/raw/health_data.csv")

    # Load and clean the data
    # air_quality_df = load_data("data/raw/air_quality.csv")
    # health_df = load_data("data/raw/health_data.csv")

    #We can directly use the dataframe instead of loading it.
    if air_quality_df is not None and health_df is not None:
        combined_df = clean_data(air_quality_df, health_df)
        save_data(combined_df, "data/processed/combined_data.csv")
    else:
        print("Data loading failed.  Cannot proceed with cleaning.")

if __name__ == "__main__":
    main()
