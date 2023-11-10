import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error

# Load the dataset
data = pd.read_csv('corruption.csv')

# Prompt the user to enter the country of interest
user_country = input("Enter the country name: ")

# Filter the dataset for the user-selected country
filtered_data = data[data['country'] == user_country]

# Check if the user-selected country exists in the dataset
if filtered_data.empty:
    print(f"Data not found for {user_country}. Please check the country name.")
else:
    # Select the relevant data column for forecasting (e.g., '2015')
    target_column = '2015'

    # Data Preprocessing
    # Convert the target column to a numerical type (if not already)
    filtered_data[target_column] = pd.to_numeric(filtered_data[target_column], errors='coerce')

    if filtered_data[target_column].isna().any():
        print("Warning: Missing values detected in the target column. Data may not be suitable for forecasting.")
    
    if len(filtered_data) < 24:  # Assuming seasonal_periods=12
        print("Warning: Insufficient data for seasonal forecasting.")

    # Split the data into training and testing sets
    train_size = int(len(filtered_data) * 0.8)
    train, test = filtered_data[:train_size], filtered_data[train_size:]

    # Create a Holt-Winters Exponential Smoothing model
    model = ExponentialSmoothing(train[target_column], seasonal='add', seasonal_periods=12, trend='add', damped=True)
    
    try:
        model_fit = model.fit()
    except ValueError as ve:
        print(f"ValueError: {ve}")
        print("It seems there is an issue with the model parameters or data. Please review the data and model configuration.")
        raise ve

    # Make predictions
    predictions = model_fit.forecast(steps=len(test))

    # Calculate and print RMSE (Root Mean Squared Error)
    rmse = np.sqrt(mean_squared_error(test[target_column], predictions))
    print(f'Root Mean Squared Error (RMSE): {rmse}')

    # Visualize the actual vs. predicted values
    plt.figure(figsize=(12, 6))
    plt.plot(train['country'], train[target_column], label='Training Data')
    plt.plot(test['country'], test[target_column], label='Actual Test Data')
    plt.plot(test['country'], predictions, label='Predicted Test Data', linestyle='--')
    plt.legend()
    plt.title(f'Time Series Forecasting for {user_country} with Holt-Winters Exponential Smoothing')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.show()
