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

class TrainBot(KnowledgeEngine):
  @Rule(Book(service='train ticket'))
  def one_way(self):
    print("BOT: You have selected train ticket. ")
    if final_chatbot:
      ticket = s.findTickets()
      ticket.printTicket()

  @Rule(Book(service='delay prediction'))
  def round_way(self):
    print("BOT: You have selected a delay prediction.")
    if final_chatbot:
      dp.display_prediction()


def check_ticket(user_input):
  user_input = user_input.lower()
  service_list = ['train ticket', 'delay prediction']    
  
  for service in service_list:
    if service in user_input:
      return service_list[service_list.index(service)]
  
  return None
  

def expert_response(user_input):
    engine = TrainBot()
    engine.reset()
    service = check_ticket(user_input)
    if service != None:
        engine.declare(Book(service=service))
        engine.run()
        return True
    
    return False

sample_user_input = "I want to find the cheapest train ticket"
print(sample_user_input)
expert_response(sample_user_input)