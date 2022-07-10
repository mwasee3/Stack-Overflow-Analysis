import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import nltk
import sklearn
import string
import re


def clean_up_data(text):
    process_output = list()
    clean_text_list = list()
    #print(text)
    # convert text to lower case
    text = text.lower()
    
    # filtering out url from the string
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    text = re.sub(url_regex, "", text) 
    
    text = re.sub("#[A-Za-z0-9_]+","", text)
    text = re.sub('[^a-zA-Z\d\s\n]', "", text)
    # Remove all numbers from the tweet
    text = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", text)
    # Remove extra white spaces from start and end of tweet
    text = text.strip()
    # Removing stop words and applying stemming to the tweets
    words = text.split()
    text = ' '.join([w for w in words if not w in nltk.corpus.stopwords.words("english")])
    ps = nltk.stem.PorterStemmer()
    
    text = text.replace("'", "")
    clean_text = text.replace("\"","")

    return clean_text


def html_parser(input_text):
    parse_text = list()
    soup = BeautifulSoup(input_text, 'html.parser')
    text_list = soup.find_all("p")
    for text in text_list:
        parse_text.append(text.text)
    parsed = " ".join(parse_text)
    return parsed


def merge_data(answers_df, questions_df, tags_df):
    grouped_tags = tags_df.groupby(['Id'])['Tag'].agg(list).reset_index()
    agg_func = {'Body':list, 'CreationDate':'first'}
    answers_df[["ParentId","Body", "CreationDate"]] = answers_df.groupby(['ParentId']).agg(agg_func).reset_index()
    questions_merge_answers = questions_df.merge(answers_df, left_on='Id', right_on='ParentId')
    merged_data = questions_merge_answers.merge(grouped_tags, left_on='Id_x', right_on='Id')
    merged_data.rename(columns={"Id_x": "Id", "OwnerUserId_x": "OwnerUserId", "Score_x": "Question_score", "Body_x": "QuestionBody", "Score_y": "Answer_score", "Body_y":"Answer"})
    
    return merged_data

def full_data():
    ans = pd.read_csv('Answers.csv', encoding = "ISO-8859-1", low_memory = False)
    ques = pd.read_csv('Questions.csv', encoding = "ISO-8859-1", low_memory = False)
    tag = pd.read_csv('Tags.csv', encoding = "ISO-8859-1", low_memory = False)
    final_df = merge_data(ans, ques, tag)
    return final_df