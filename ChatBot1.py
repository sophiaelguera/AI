from chatterbot import ChatBot
import scraper as s
import DelayPrediction as dp
from scraper import Ticket 
from nlp import check_intention_by_keyword
import time



chatbot = ChatBot('Mr. Chatbot', trainer = "chatterbot.corpus.english.greetings")

services = {"train ticket": s.findTickets,
            "delay prediction": dp.display_prediction}


# information chatbot needs to collect:
    # from_station
    # to_station
    # departure_date
    # departure_time
    # return_date
    # return_time



def main():

    while True:

        
        request = input("Human: ")

        intention = check_intention_by_keyword(request)


        if intention.lower() in services and intention.lower() != "delay prediction":
            c = services[intention.lower()]()
            c.printTicket()
            print("Completed Service")
        if intention.lower() == "delay prediction":
            services[intention.lower()]()
            print("Completed Service")
            
    
        else:
            # response = str(chatbot.get_response(request))
            print("Bot: Sorry I don't understand that. Please rephrase your statement.")


if __name__ == '__main__':
    try:
        time.sleep(0.5)
        print("Welcome, I'm a chatbot built to help you travel, how can I help you today?")
        main()

    except KeyboardInterrupt :
        print("Program Interrupted")

