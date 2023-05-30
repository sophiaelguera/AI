import scraper as s
import DelayPrediction as dp
from scraper import Ticket 
from nlp import check_intention_by_keyword
import time
from Engine import *

services = {"train ticket": s.findTickets,
            "delay prediction": dp.display_prediction}

def main():

    final_chatbot = True
    flag=True
    print("BOT: Hi there! How can I help you?.\n (If you want to exit, just type bye!)") 
    while(flag==True):  
       
        user_input = input("Human: ")

        intention = check_intention_by_keyword(user_input)

        if intention == 'goodbye':
            flag=False
        elif intention != None:
            if not expert_response(user_input):
                
                if intention.lower() in services and intention.lower() != "delay prediction":
                    c = services[intention.lower()]()
                    c.printTicket()
                    print("Completed Service")
                elif intention.lower() == "delay prediction":
                    services[intention.lower()]()
                    print("Completed Service")


        else: 
            print("BOT: Sorry I don't understand that. Please rephrase your statement.")
        

              
if __name__ == '__main__':
    try:
        time.sleep(0.5)
        main()
        print("Service Completed\n BOT: Can I help with anything else?")

    except KeyboardInterrupt :
        print("Program Interrupted")