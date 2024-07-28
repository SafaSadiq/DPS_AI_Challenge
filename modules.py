import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

def preproc(data):
    data = data[data.columns[:5]] #keep only first 5 columns
    data = data.fillna(0) #replace NULL values with 0

    #split data before and after 2020
    accidents_after_2020 = data[data["JAHR"]>2020]
    accidents_until_2020 = data[data["JAHR"]<=2020]


    #Remove "Summe" from "MONAT" and create another df for "Summe" values
    accidents_until_2020_by_year = accidents_until_2020[accidents_until_2020["MONAT"]== "Summe"].drop(columns="MONAT")
    accidents_until_2020 = accidents_until_2020[accidents_until_2020["MONAT"]!= "Summe"].drop(columns="JAHR")

    accidents_after_2020_by_year = accidents_after_2020[accidents_after_2020["MONAT"]== "Summe"].drop(columns="MONAT")
    accidents_after_2020 = accidents_after_2020[accidents_after_2020["MONAT"]!= "Summe"].drop(columns="JAHR")


    #convert "MONAT" from String to DateTime
    accidents_until_2020["MONAT"] = pd.to_datetime(accidents_until_2020["MONAT"], format='%Y%m')
    accidents_after_2020["MONAT"] = pd.to_datetime(accidents_after_2020["MONAT"], format='%Y%m')

    return accidents_until_2020, accidents_after_2020, accidents_until_2020_by_year, accidents_after_2020_by_year

    # print(accidents["MONATSZAHL"].unique())
    # print("___________________________________")
    # print(accidents["AUSPRAEGUNG"].unique())
    # print("___________________________________")
    # print(accidents["JAHR"].unique())
    # print("___________________________________")
    # print(accidents["MONAT"].unique())


def plot_total_accidents(data, save=False):
    # Aggregate data to get the total number of accidents per accident type and category
    aggregated_data = data.groupby(['MONATSZAHL', 'AUSPRAEGUNG'])['WERT'].sum().reset_index()

    # Plot the data
    plt.figure(figsize=(14, 8))
    sns.barplot(data=aggregated_data, x='MONATSZAHL', y='WERT', hue='AUSPRAEGUNG')
    plt.title('Total Number of Accidents per Accident Type and Category')
    plt.xlabel('Accident Type', fontsize=16)
    plt.ylabel('Total Number of Accidents', fontsize=16)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.legend(title='Category', fontsize=16)
    plt.grid(False)
    if save:
        plt.savefig("Visualizations/TotalAccidentsByTypeAndCategory.png")
    plt.show()


def plot_accidents_over_time(data, type="insgesamt", save=False):

    aggregated_data = data[data["AUSPRAEGUNG"]==type].groupby(['MONATSZAHL', 'JAHR'])['WERT'].sum().reset_index()
    monatszahl = data["MONATSZAHL"].unique()

    fig, ax = plt.subplots(1,len(monatszahl), figsize=(15, 5))

    for i in range(len(monatszahl)):
        subset = aggregated_data[aggregated_data['MONATSZAHL']==monatszahl[i]]
        ax[i].title.set_text("Category = "+ monatszahl[i])
        ax[i].set_xlabel("Year")
        ax[i].set_ylabel("Number of Accidents")
        ax[i].plot(subset['JAHR'].values, subset['WERT'].values, marker='o')

    if save:
        plt.savefig("Visualizations/Accidents(" + type + ")ByYear.png")


def create_Time_series_data(data, category, type):
    data_subset = data[
        (data["MONATSZAHL"]==category)
        &
        (data["AUSPRAEGUNG"]==type)
        ].drop(columns=["MONATSZAHL","AUSPRAEGUNG"])

    data_subset = data_subset.set_index('MONAT')

    data_subset = data_subset.sort_values(by=['MONAT'])

    return data_subset

def find_best_params(train_set, p_values, d_values, q_values):
    params = []
    mse_train_set = []

    for p in p_values:
        for d in d_values:
            for q in q_values:

                try:
                    model = ARIMA(train_set, order=(p,d,q))
                    model_fit = model.fit()
                    predict = model_fit.predict()
                    mse = mean_squared_error(predict, train_set)

                    params.append((p,d,q))
                    mse_train_set.append(mse)
                except:
                    continue

    lowest_mse_index = mse_train_set.index(min(mse_train_set))

    return params[lowest_mse_index]