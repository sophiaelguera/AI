from chatterbot import ChatBot
import scraper as s
import DelayPrediction as dp
from scraper import Ticket 
from nlp import check_intention_by_keyword
import time
from Engine import *


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
                print("BOT: Sorry I don't understand that. Please rephrase your statement.")
        

              
if __name__ == '__main__':
    try:
        time.sleep(0.5)
        main()

    except KeyboardInterrupt :
        print("Program Interrupted")