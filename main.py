import json

from flask import Flask, request, jsonify
from modules import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_model(request):

    #read data and preprocess dataset on to keep values after 2020 and for Category: 'Alkoholunfälle' amd Type: 'insgesamt
    accidents = pd.read_csv("monatszahlen2405_verkehrsunfaelle_export_31_05_24_r.csv")
    accidents_until_2020, _,_,_ = preproc(accidents)
    train_set = create_Time_series_data(accidents_until_2020, 'Alkoholunfälle', 'insgesamt')

    #fit best model found using grid search
    best_model = ARIMA(train_set, order=(6,0,4))
    best_model_fit = best_model.fit()

    #find train predictions
    prediction_train_set = best_model_fit.predict()

    #Forecast the future values for 12 months
    forecast = best_model_fit.get_forecast(steps=12)
    forecast_df = forecast.summary_frame()

    #read request info to find which prediction is required and return that value
    data = request.get_json()

    year = data["year"]
    month = data["month"]

    dt = year + "-" + month
    dt = pd.to_datetime(dt, format='%Y-%m')

    all_predictions = pd.concat([prediction_train_set, forecast_df["mean"]])

    predicted_value = all_predictions.loc[dt]

    response = {
        "prediction": predicted_value
    }
    return jsonify(response)



