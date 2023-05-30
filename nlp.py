import random
import json
import spacy
import difflib
from difflib import get_close_matches, SequenceMatcher
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from dateutil import parser

from random import choice
from experta import *

import spacy.cli
# spacy.cli.download("en_core_web_sm")

def dateFormat(date):

    cleaned_user_date = lemmatize_and_clean(date)
        # Parse the user input using dateutil.parser
    date_obj = parser.parse(cleaned_user_date)

    # Format the date as DDMMYYYY
    formatted_date = date_obj.strftime("%d%m%Y")
    # print("Formatted date:", formatted_date)
    return formatted_date

    

    # except ValueError:
    #     print("Invalid date. Please enter a valid date.")

def timeFormat(time):
    try:
        cleaned_user_time = lemmatize_and_clean(time)
        # Parse the user input using dateutil.parser
        time_obj = parser.parse(cleaned_user_time, default=datetime.now())

        # Format the time as 2000
        formatted_time = time_obj.strftime("%H%M")

        return formatted_time
    except ValueError:
        print("Invalid time. Please enter a valid time.")

intentions_path = "intentions.json"
sentences_path = "sentences.txt"

with open(intentions_path) as f:
    intentions = json.load(f)

# print(json.dumps(intentions, indent=4))

final_chatbot = False


def check_intention_by_keyword(sentence):

        for type_of_intention in intentions:
            if sentence.lower() in intentions[type_of_intention]["patterns"]:
                # print("BOT: " + random.choice(intentions[type_of_intention]["responses"]))
                
                # # Do not change these lines
                # if type_of_intention == 'greeting' and final_chatbot:
                #     print("BOT: We can talk about train tickets and train delays, How can I help? \n")
                return type_of_intention
 


# sample_user_input = "train ticket"
# print(sample_user_input)
# print(f'Detected intention: {check_intention_by_keyword(sample_user_input)}')
# print('*' * 50)
# sample_user_input = "I would like to buy a train ticket"
# print(sample_user_input)
# print(f'Detected intention: {check_intention_by_keyword(sample_user_input)}')

# Reading `sentences.txt` file and printing its content.
time_sentences = ''
date_sentences = ''
with open(sentences_path) as file:
    for line in file:
        parts = line.split(' | ')
        if parts[0] == 'time':
            time_sentences = time_sentences + ' ' + parts[1].strip()
        elif parts[0] == 'date':
            date_sentences = date_sentences + ' ' + parts[1].strip()

# print(time_sentences)
# print('*' * 50)
# print(date_sentences)

nlp = spacy.load('en_core_web_sm')

labels = []
sentences = []

doc = nlp(time_sentences)
for sentence in doc.sents:
    labels.append("time")
    sentences.append(sentence.text.lower().strip())

doc = nlp(date_sentences)
for sentence in doc.sents:
    labels.append("date")
    sentences.append(sentence.text.lower().strip())

# for lable, sentence in zip(labels, sentences):
#      print(lable + " : " + sentence)



def lemmatize_and_clean(text):
    doc = nlp(text.lower())
    out = ""
    for token in doc:
        if not token.is_stop and not token.is_punct:
            out = out + token.lemma_ + " "
    return out.strip()

sample_user_input = "after 1500"
print(lemmatize_and_clean(sample_user_input))


final_chatbot = False

def date_time_response(user_input):
    cleaned_user_input = lemmatize_and_clean(user_input)
    doc_1 = nlp(cleaned_user_input)
    similarities = {}
    for idx, sentence in enumerate(sentences):
        cleaned_sentence = lemmatize_and_clean(sentence)
        doc_2 = nlp(cleaned_sentence)
        similarity = doc_1.similarity(doc_2)
        similarities[idx] = similarity

    max_similarity_idx = max(similarities, key=similarities.get)
    
    # Minimum acceptable similarity between user's input and our Chatbot data
    # This number can be changed
    min_similarity = 0.75

    # Do not change these lines
    if similarities[max_similarity_idx] > min_similarity:
        if labels[max_similarity_idx] == 'time':
            print("BOT: " + "It’s " + str(datetime.now().strftime('%H:%M:%S')))
            if final_chatbot:
                print("BOT: You can also ask me what the date is today. (Hint: What is the date today?)")
        elif labels[max_similarity_idx] == 'date':
            print("BOT: " + "It’s " + str(datetime.now().strftime('%Y-%m-%d')))
            if final_chatbot:
                print("BOT: Now can you tell me where you want to go? (Hints: you can type in a city's name, or an organisation. I am going to London or I want to visit the University of East Anglia.)")
        return True
    
    return False

# sample_user_input = "Tell me the time!"
# print(sample_user_input)
# date_time_response(sample_user_input)

# user_input = input("Enter a date: ")

