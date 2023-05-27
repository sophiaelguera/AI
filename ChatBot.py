from chatterbot import ChatBot
from googletrans import Translator as tl
from wit import Wit as wit
import IndividualStock as singleStock
import ActiveStock as activeStocks
import scraper as s
import DelayPrediction as dp
from scraper import Ticket 
from nlp import check_intention_by_keyword
import time




chatbot = ChatBot('Mr. Chatbot', trainer = "chatterbot.corpus.english.greetings")

services = {"search for a stock":singleStock.findStock,
            "search for active stocks":activeStocks.findMostActiveStocks,
            "train ticket": s.findTickets,
            "delay prediction": dp.display_prediction}


# information chatbot needs to collect:
    # from_station
    # to_station
    # departure_date
    # departure_time
    # return_date
    # return_time

def main():
    # print("What language would you like your text translated to?")
    # lang = wit.interactive().lower()

    while True:

        
        request = input("Human: ")

        intention = check_intention_by_keyword(request)

        if intention.lower() in services and not "delay prediction":
            c = services[intention.lower()]()
            c.printTicket()
            print("Completed Service")
        if intention.lower() == "delay prediction":
            services[intention.lower()]()
        else:
            response = str(chatbot.get_response(request))
            print("Bot: " + response)


if __name__ == '__main__':
    try:
        time.sleep(0.5)
        print("Welcome")
        main()

    except KeyboardInterrupt :
        print("Program Interrupted")

