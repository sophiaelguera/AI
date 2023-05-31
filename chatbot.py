import scraper as s
import DelayPrediction as dp
from scraper import Ticket 
from nlp import check_intention_by_keyword
import time
from Engine import *

# services chatbot provides
services = {"train ticket": s.findTickets,
            "delay prediction": dp.display_prediction}

# Main function to run the chatbot
def main():

    final_chatbot = True
    flag=True
    print("\n\n")
    # Begins conversation
    print("Bot: Hi there! How can I help you?.\n (If you want to exit, just type bye!)") 
    while(flag==True):  
       
        user_input = input("Human: ")
        # recognizing intent
        intention = check_intention_by_keyword(user_input)
        # to exit chatbot
        if intention == 'goodbye':
            flag=False
        
        elif intention != None:
            # checking if intent is in the knowledge base and reasoning engine and if it is it will run the correct response and service
            if not expert_response(user_input):
                # if not in the KB and Reasoning Engine it will check intentions.json for all intents and then run correct service
                if intention.lower() in services and intention.lower() != "delay prediction":
                    c = services[intention.lower()]()
                    c.printTicket()

                elif intention.lower() == "delay prediction":
                    services[intention.lower()]()


        # error handling if user input is not expected 
        # prompts user to type command again
        else: 
            print("Bot: Sorry I don't understand that. Please rephrase your statement.")
        

# Running Chatbot!   
if __name__ == '__main__':
    try:
        time.sleep(0.5)
        main()
        print("Service Completed")

    except KeyboardInterrupt :
        print("Program Interrupted")