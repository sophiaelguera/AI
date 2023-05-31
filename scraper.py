from bs4 import BeautifulSoup
import requests
import json


from csvReader import findStationABV
from csvReader import findSpecificStation

from nlp import dateFormat
from nlp import timeFormat
from nlp import arriveBy

# information chatbot needs to collect from user through conversation:
    # from_station
    # to_station
    # departure_date
    # departure_time
    # return_date
    # return_time

# Ticket class to store all the information gathered about the cheapest train ticket and a method to print the ticket so the user can see and access it
class Ticket:
    def __init__(self, from_station, to_station, departure_date, departure_time, return_date,  return_time, ticketPrice, ticketType, url):
        self.from_station = from_station
        self.to_station = to_station
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.return_date = return_date
        self.return_time = return_time
        self.ticketPrice = ticketPrice
        self.ticketType = ticketType
        self.url = url
    
    def printTicket(self):
        print("\nThe cheapest ticket for your journey is:\n" 
              + "Departing from:    " + self.from_station + "\n" +
               "Arriving at:    " + self.to_station + "\n" +
               "Departure Date:    " + self.departure_date + "\n" +
               "Departure Time:    " + self.departure_time + "\n" +
               "Return Date:    " + self.return_date + "\n" +
               "Return Time:    " + self.return_time + "\n" +
               "Ticket Price:    " + self.ticketPrice + "\n" +
               "Ticket Type:     " + self.ticketType + "\n" +
               "Url:          " + self.url)

# Method to prompt the user through a conversation about their journey and gather all necessary info
# This method then creates a url for the user journey that corresponds to the journey on the national rail website
# Then the website parses through the json to find the tickets presented on that page
# Calls on findCheapestTickets(tickets) to find the cheapest ticket from the journeys on the page
# Creates a Ticket object that stores all the necessary info and returns it
def findTickets():
    #Ask what ..
    from_station = input('Bot: Can you tell me the name of the station you would like to depart from?\nHuman: ')  
    
    from_stations = findSpecificStation(from_station)

    if len(from_stations) > 1:
        print('Bot: There are a couple of station that match that name:')
        for station in from_stations:
            print(station)
        from_station = input('Bot: Which of the above stations would you like to go to? \nHuman: ') 
        from_station = findStationABV(from_station)
    else:
        from_station = from_stations[0]

    #Ask what ..
    to_station = input('Bot: Enter the name of the station you would like to go: \nHuman: ')    
    #Ask what ...
    to_stations = findSpecificStation(to_station)
    
    if len(to_stations) > 1 and to_stations != 'London':
        print('Bot: There are a couple of station that match that name:')
        for station in to_stations:
            print(station)
        to_station = input('Bot: Which of the above stations would you like to go to? \nHuman: ') 
        to_station = findStationABV(to_station)
    elif to_stations == 'London':
        to_station == 'London'
    else:
        to_station = to_stations[0]

    #Ask what ...
    departure_date = input('Bot: What day you would like to depart? \nHuman: ') 
    #Ask what ...
    if str(departure_date) != 'today' and str(departure_date) !=  'tomorrow':
        departure_date = dateFormat(str(departure_date))   
    #Ask what..
    departure_time = input('Bot: What time you would like to depart: \nHuman: ')

    departure_time = timeFormat(departure_time)

    arrive = arriveBy(departure_time)
    #Ask what..
    return_date = input('Bot: What date would you like to return or type None if you would like a single ticket: \nHuman:')   
    #Ask what..
    if str(return_date) != 'today' and str(return_date) !=  'tomorrow' and str(return_date) != "None":
        return_date = dateFormat(str(return_date))
        arrive = arriveBy(return_date)
    elif str(return_date) == "None":
        return_date = None


    # form url to scrape
    if return_date == None or return_date == "None":
        html_page = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{from_station}/{to_station}/{departure_date}/{departure_time}/dep'''
        ticketType = 'single'
        # print(html_page)
    else:
        return_time = input('Enter the time you would like to return: \nHuman:')
        return_time = timeFormat(return_time)
        html_page = f'''https://ojp.nationalrail.co.uk/service/timesandfares/{from_station}/{to_station}/{departure_date}/{departure_time}/{arrive}/{return_date}/{return_time}/{arrive}'''
        # print(html_page)
        ticketType = 'return'

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


    theCheapestTicket = Ticket(from_station, to_station, departure_date, str(departure_time), return_date, str(return_time), str(ticketPrice), ticketType, str(html_page))

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

