import json
import spacy
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from dateutil import parser

from random import choice
from experta import *

import spacy.cli
# spacy.cli.download("en_core_web_sm")

# Method created to format user inputted date in any format and return the correct format needed for web scraping
# format needed is DDMMYYYY
def dateFormat(date):

    cleaned_user_date = lemmatize_and_clean(date)
        # Parse the user input using dateutil.parser
    date_obj = parser.parse(cleaned_user_date)

    # Format the date as DDMMYYYY
    formatted_date = date_obj.strftime("%d%m%Y")
    # print("Formatted date:", formatted_date)
    return formatted_date

# Method created to format user inputted time in any format and return the correct format needed for web scraping
# format needed is 2000
def timeFormat(time):
    cleaned_user_time = lemmatize_and_clean(time)
    # Parse the user input using dateutil.parser
    time_obj = parser.parse(cleaned_user_time, default=datetime.now())

    # Format the time as 2000
    formatted_time = time_obj.strftime("%H%M")

    return formatted_time

# Method to handle key words like before 
# If user would like to arrive at the destination before a certain time this method returns 
# the correct key word for the url and web scraping
def arriveBy(time):
    if 'before' in time:
        arriveBy = 'arr'
    else:
        arriveBy = 'dep'
    return arriveBy


intentions_path = "intentions.json"
sentences_path = "sentences.txt"

with open(intentions_path) as f:
    intentions = json.load(f)

final_chatbot = False

# Method to check the intention of the user input, returns the type of intention
def check_intention_by_keyword(sentence):
        for type_of_intention in intentions:
            if sentence.lower() in intentions[type_of_intention]["patterns"]:
                return type_of_intention



# Method to clean user input and remove stop words and punctuation
nlp = spacy.load('en_core_web_sm')
def lemmatize_and_clean(text):
    doc = nlp(text.lower())
    out = ""
    for token in doc:
        if not token.is_stop and not token.is_punct:
            out = out + token.lemma_ + " "
    return out.strip()



