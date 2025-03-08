# src/utils.py
import pandas as pd

def load_data(filepath):
    """Loads data from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def save_data(df, filepath):
    """Saves a Pandas DataFrame to a CSV file."""
    try:
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    except Exception as e:
        print(f"Error saving data: {e}")


def check_missing_values(df):
    """Checks for and reports missing values in a DataFrame."""
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("Missing Values:")
        print(missing_values[missing_values > 0])
    else:
        print("No missing values found.")
