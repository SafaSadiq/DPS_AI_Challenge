# DPS_AI_Challenge

The goal of this challenge was to create a prediction model using “Monatszahlen Verkehrsunfälle” Dataset to predict the number of accidents of a certain type and category on a specified month.

### Mission 1: Create a AI Model
The data is preprocessed to split the dataset into values before 2020 and after 2020. The "Summe" values are removed from the "Monat" column and the "Monat" column is converted from string into datetime format.

The model created is the ARIMA model which stands for AutoRegressive Integrated Moving Average, is a popular and versatile statistical method used for time series forecasting. 

The best parameters for the model are found using grid search to avoid excessive tuning. 

Predictions are found for the next 12 months, starting from January 2021.

### Mission 2: Publish your source code & Deploy

The model is deployed at this endpoint: https://us-central1-dpsaichallenge.cloudfunctions.net/dpsaichallenge and has predictions from January 2000 to December 2021.

To get predictions from the model, send a POST request with a JSON body of this format: {"year": "xxxx", "month": "xx"}.
Alternatively, you can run the file getPredictionsFromModel.py

### Mission 3: Send us the URL of your work

Submission file: Submission.py
