import joblib
import numpy as np
from csvReader import findStationLongABV
import json
import datetime


def calculate_delay(station, delay, destination_station):
    loaded_model = joblib.load('knn_model.pkl')
    user_input = np.array([[station, int(delay)]])  # Update with your input for 'tpl' and 'arr_delay'
    # Predict using the loaded model
    predicted_delay = loaded_model.predict(user_input)
    return predicted_delay[0][destination_station]


def display_prediction():
    station = input("Bot: What station are you waiting at? ")
    delay = int(input("Bot: How many minutes is the oncoming train delayed by? "))
    destination_station = input("Bot: Where is your destination? ")

    with open('tpl_dict.txt', 'r') as file:
        tpl_dict = json.load(file)

    station_abv = findStationLongABV(station)
    dest_station_abv = findStationLongABV(destination_station)

    with open('link_times.txt', 'r') as file:
        link_times = json.load(file)

    time_diff = link_times[dest_station_abv] - link_times[station_abv]
    delay = round(calculate_delay(tpl_dict[station_abv], delay,
                                  tpl_dict[dest_station_abv]))
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


'''with open('tpl_dict.txt', 'r') as file:
        tpl_dict = json.load(file)

with open('link_times.txt', 'r') as file:
    link_times = json.load(file)

print(link_times[findStationLongABV("weymouth")])'''

#print(datetime.datetime.now())