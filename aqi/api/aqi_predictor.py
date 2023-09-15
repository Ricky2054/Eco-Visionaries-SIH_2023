import pandas as pd
import numpy as np
import datetime
import json

import statsmodels.api as sm
from statsmodels.tsa.statespace.sarimax import SARIMAX

import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.conf  import settings

# Specify the absolute path to your CSV file
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'static/data/pollutants.csv')



# Load your CSV data
data = pd.read_csv(CSV_FILE_PATH)


data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, format='mixed')
data.set_index('Date', inplace=True)

# Define the columns for prediction
target_columns = ['PM10', 'NO2', 'SO2']

# Define a function to train SARIMAX models for each target
def train_sarimax_model(data, target_column):

    try:
        # Split the data into training and testing sets (you can adjust the split ratio)
        train_size = int(len(data) * 0.8)
        train_data = data[target_column][:train_size]
        test_data = data[target_column][train_size:]

        # Fit a SARIMAX model
        model = sm.tsa.SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        results = model.fit()

        return results
    
    except Exception as e:
        print(e)
        return None

# Function to predict data for the next 7 days from a given date
def predict_next_7_days_pollutants(start_date=datetime.datetime.today()+datetime.timedelta(days=1)):
    try:
        
        start_date = pd.to_datetime(start_date)

        future_predictions = {}
        for i in range(7):
            predictions = {}
            for column in target_columns:
                model = train_sarimax_model(data, column)
                future_date = start_date + pd.DateOffset(days=i)
                forecast = model.get_forecast(steps=1, exog=np.array([1]))  # Add exogenous variables if needed
                future_prediction = forecast.predicted_mean[0]
                predictions[column] = future_prediction
            future_predictions[future_date.strftime('%d-%m-%Y')] = predictions

                
        json_predictions = json.dumps(future_predictions, indent=4)
        return json_predictions
    
    except Exception as e:
        print(e)
        return None


