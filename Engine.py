from random import choice
from experta import *
import spacy.cli
# spacy.cli.download("en_core_web_sm")
import scraper as s
import DelayPrediction as dp

final_chatbot = True

class Book(Fact):
    """Info about the chatbot services."""
    pass

# Set of rules to recognize intent and part of the reasongin engine of the chatbot
# Based on the rules the chat bot can make a desicion on which service the user is requesting based on their intent
class TrainBot(KnowledgeEngine):
  @Rule(Book(service='train ticket'))
  def one_way(self):
    print("\nBot: Ok! I will need a little bit of information about your journey! ")
    if final_chatbot:
      ticket = s.findTickets()
      ticket.printTicket()
      print("\nBot: you may click the link above to purchase you train ticket, safe travels!\n")
      print("Bot: Can I help you with anything else?")

  @Rule(Book(service='delay prediction'))
  def round_way(self):
    print("Bot: You have selected a delay prediction.")
    if final_chatbot:
      dp.display_prediction()
      print("\nBot: Can I help you with anything else?")

# method to decide which service the user is requesting and returning it.
def check_ticket(user_input):
  user_input = user_input.lower()
  service_list = ['train ticket', 'delay prediction']    
  
  for service in service_list:
    if service in user_input:
      return service_list[service_list.index(service)]
  
  return None
  
# method to generate the response based on the intent and reasoning 
def expert_response(user_input):
    engine = TrainBot()
    engine.reset()
    service = check_ticket(user_input)
    if service != None:
        engine.declare(Book(service=service))
        engine.run()
        return True
    
    return False
