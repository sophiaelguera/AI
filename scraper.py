import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import re

from csvReader import findStationABV

# information chatbot needs to collect:
    # from_station
    # to_station
    # departure_date
    # departure_time
    # return_date
    # return_time

class Ticket:
    def __init__(self, from_station, to_station, departure_date, departure_time, return_date,  return_time, ticketPrice, ticketType):
        self.from_station = from_station
        self.to_station = to_station
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.return_date = return_date
        self.return_time = return_time
        self.ticketPrice = ticketPrice
        self.ticketType = ticketType
    
    def printTicket(self):
        print("\nThe cheapest ticket for the date and times you provided is:\n" 
              + "Dparting from:    " + self.from_station + "\n" +
               "Arriving at:    " + self.to_station + "\n" +
               "Departure Date:    " + self.departure_date + "\n" +
               "Departure Time:    " + self.departure_time + "\n" +
               "Return Date:    " + self.return_date + "\n" +
               "Return Time:    " + self.return_time + "\n" +
               "Ticket Price:    " + self.ticketPrice + "\n" +
               "Ticket Type:     " + self.ticketType)



def findTickets():
    #Ask what ..
    from_station = input('Bot: Enter the name of the station you would like to depart from?\nHuman: ')

    from_station = findStationABV(from_station)    

    #Ask what ..
    to_station = input('Bot: Enter the name of the station you would like to go: \nHuman: ')    

    to_station = findStationABV(to_station)

    #Ask what ...
    departure_date = input('Bot: Enter the date you would like to depart: \nHuman: ')    
    #Ask what..
    departure_time = input('Bot: Enter the time you would like to depart: \nHuman: ')
    #Ask what..
    return_date = input('Bot: Enter the date you would like to return or None: \n Human:')   
    #Ask what..
    if return_date != "None":
        return_time = input('Enter the time you would like to return: Human:')
        html_page = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{from_station}/{to_station}/{departure_date}/{departure_time}/dep/{return_date}/{return_time}/dep'''
        print(html_page)
        ticketType = 'return'
    else:
        html_page = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{from_station}/{to_station}/{departure_date}/{departure_time}/dep/{return_date}/{return_time}/dep'''
        ticketType = 'single'

    #Parse the html using beautfil soup and store in the variable 'soup'
    soup = BeautifulSoup(requests.get(html_page).text, 'html.parser')

    #Get the price
    allTickets = soup.find_all('script', attrs={'type':'application/json'})

    raw_tickets = [json.loads(ticket.string) for ticket in allTickets]

    tickets = []

    for ticket in raw_tickets:
        if ticket['returnJsonFareBreakdowns'] != []:
            tickets.append(ticket)
    

    ## Now u need to look through each ticket in list to find the cheapest one and then print all the details.

    cheapTicket = findCheapestTickets(tickets)


    from_station = cheapTicket['jsonJourneyBreakdown']['departureStationName']
    to_station = cheapTicket['jsonJourneyBreakdown']['arrivalStationName']
    departure_time = cheapTicket['jsonJourneyBreakdown']['departureTime']
    return_time = cheapTicket['jsonJourneyBreakdown']['arrivalTime']

    for i in cheapTicket['returnJsonFareBreakdowns']:
        for l, j in i.items():
            if l == 'ticketPrice':
                ticketPrice = j


    theCheapestTicket = Ticket(from_station, to_station, departure_date, str(departure_time), return_date, str(return_time), str(ticketPrice), ticketType)

    return theCheapestTicket


def findCheapestTickets(tickets):
    cheapestFare = 9999999

    for ticket in tickets:

        ticketFare = ticket['returnJsonFareBreakdowns']
        for fare in ticketFare:
            if fare['ticketPrice'] < cheapestFare:
                cheapestFare = fare['ticketPrice']
                cheapestTicket = ticket
    

    return cheapestTicket














# url = f'''https://ojp.nationalrail.co.uk/service/timesandfares/NRW/BFR/today/1215/dep'''

# f = requests.get(url)

# soup = BeautifulSoup(f.text, features="html.parser")

# # print(soup.get_text())

# for i in soup.findAll("div",{"class":"single clear false has-alt-trains"}):
#     print((i.find("span",{"class":"fare-breakdown"})).text)

# journey_type = "single"
# return_date= "11/05/2023"

# if return_date == None:
#     url = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{"NRW"}/{"LGX"}/{"today"}/{"12:15"}/dep'''
# else:
#     journey_type = "return"
#     # url = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{from_station}/{to_station}/{departure_date}/{departure_time}/dep/{return_date}/{return_time}/dep'''    