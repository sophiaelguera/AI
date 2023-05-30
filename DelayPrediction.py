import joblib
import numpy as np
from csvReader import findStationLongABV
import json
import datetime


def calculate_delay(station, delay, destination_station):
    loaded_model = joblib.load('knn_model.pkl')  # loads prediction model
    user_input = np.array([[station, int(delay)]])  # converts information taken from user to a model_input
    predicted_delay = loaded_model.predict(user_input)  # predicts delay using model_input on the prediction model
    return predicted_delay[0][destination_station]


def display_prediction():
    # data collection from user
    station = input("Bot: What station are you waiting at? ")
    delay = int(input("Bot: How many minutes is the oncoming train delayed by? "))
    destination_station = input("Bot: Where is your destination? ")

    with open('tpl_dict.txt', 'r') as file:  # reads in tpl_dict
        tpl_dict = json.load(file)

    station_abv = findStationLongABV(station)  # converts data to format used by model
    dest_station_abv = findStationLongABV(destination_station)

    with open('link_times.txt', 'r') as file:  # reads in link_times
        link_times = json.load(file)

    time_diff = link_times[dest_station_abv] - link_times[station_abv]  # calcs time typical time between stations
    delay = round(calculate_delay(tpl_dict[station_abv], delay,
                                  tpl_dict[dest_station_abv]))  # calcs delay with data provided by user
    if delay > 0:
        print("Bot: You should expect to arrive in " + destination_station + " " + str(delay) +
        " minutes later than scheduled: "
        + str((datetime.datetime.now()+datetime.timedelta(minutes=time_diff+delay)).strftime("%H:%M")))
    if delay == 0:
        print("Bot: You should expect to arrive in " + destination_station + "on time: "
        + str((datetime.datetime.now()+datetime.timedelta(minutes=time_diff+delay)).strftime("%H:%M")))
    if delay < 0:
        print("Bot: You should expect to arrive in " + destination_station + " " + str(delay) +
        " minutes earlier than scheduled: "
        + str((datetime.datetime.now()+datetime.timedelta(minutes=time_diff+delay)).strftime("%H:%M")))