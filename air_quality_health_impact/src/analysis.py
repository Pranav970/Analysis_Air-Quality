# src/analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import load_data
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


def perform_eda(df):
    """Performs exploratory data analysis (EDA)."""

    # Descriptive statistics
    print("Descriptive Statistics:\n", df.describe())

    # Histograms
    df.hist(figsize=(12, 8))
    plt.suptitle("Histograms of Variables")
    plt.tight_layout()
    plt.show()

    # Correlation matrix
    corr_matrix = df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

    # Time series plots
    plt.figure(figsize=(14, 6))
    plt.plot(df['date'], df['PM2.5'], label='PM2.5')
    plt.plot(df['date'], df['hospital_admissions'], label='Hospital Admissions')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Time Series of PM2.5 and Hospital Admissions')
    plt.legend()
    plt.show()

    # Scatter plots (PM2.5 vs. hospital admissions)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='PM2.5', y='hospital_admissions', data=df)
    plt.title('PM2.5 vs. Hospital Admissions')
    plt.show()

def perform_regression_analysis(df):
    """Performs linear regression analysis."""

    # Prepare the data
    X = df[['PM2.5', 'NO2', 'O3']]  # Independent variables
    y = df['hospital_admissions']    # Dependent variable

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 80/20 split

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")

    # Display coefficients
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)

    # Feature importance (based on coefficients)
    feature_importance = pd.Series(model.coef_, index=X.columns)
    feature_importance.sort_values(ascending=False).plot(kind='bar')
    plt.title("Feature Importance")
    plt.show()



def main():
    # Load the processed data
    df = load_data("data/processed/combined_data.csv")

    if df is not None:
         # Convert 'date' column to datetime objects
        df['date'] = pd.to_datetime(df['date'])
        perform_eda(df)
        perform_regression_analysis(df)
    else:
        print("Data loading failed.  Cannot proceed with analysis.")

if __name__ == "__main__":
    main()
