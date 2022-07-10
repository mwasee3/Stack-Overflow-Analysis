import requests
import csv
import json
import pandas as pd
import datetime
import time


def get_questions(from_date,to_date,order):
    has_more = True
    
    utc_from_date=datetime.datetime(int(from_date[0:4]),int(from_date[5:7]),int(from_date[8:10]))
    utc_from_date=(((int(utc_from_date.strftime("%Y"))-int(1970))*365)+int(utc_from_date.strftime("%d")))*24*60*60
    
    utc_to_date=datetime.datetime(int(to_date[0:4]),int(to_date[5:7]),int(to_date[8:10]))
    utc_to_date=(((int(utc_to_date.strftime("%Y"))-int(1970))*365)+int(utc_to_date.strftime("%d")))*24*60*60
    
    while has_more:
        x = 1
        url="https://api.stackexchange.com/2.3/questions?page=%s&pagesize=100&fromdate=%s&todate=%s&order=%s&sort=creation&site=stackoverflow&key=uvLkWOoIdmLvryg2A2L)LQ((" % (str(x),utc_from_date,utc_to_date,order)
        response = requests.get(url)
        response=response.json()
        has_more = response["has_more"]
        if has_more == True:
            has_more = True
        else:
            has_more = False
        x += 1
        df = pd.DataFrame.from_dict(response)
        df.to_csv(r'questions.csv',index="origin",mode="a",header=False)
        
def get_answers(from_date,to_date,order):
    has_more = True
   
    utc_from_date=datetime.datetime(int(from_date[0:4]),int(from_date[5:7]),int(from_date[8:10]))
    utc_from_date=(((int(utc_from_date.strftime("%Y"))-int(1970))*365)+int(utc_from_date.strftime("%d")))*24*60*60
    
    utc_to_date=datetime.datetime(int(to_date[0:4]),int(to_date[5:7]),int(to_date[8:10]))
    utc_to_date=(((int(utc_to_date.strftime("%Y"))-int(1970))*365)+int(utc_to_date.strftime("%d")))*24*60*60
    
    while has_more:
        x = 1
        url="https://api.stackexchange.com/2.3/answers?page=%s&pagesize=100&fromdate=1523059200&todate=1649289600&order=desc&sort=creation&site=stackoverflow&key=uvLkWOoIdmLvryg2A2L)LQ((" % (str(x),utc_from_date,utc_to_date,order)
        response = requests.get(url)
        response=response.json()
        has_more = response["has_more"]
        if has_more == True:
            has_more = True
        else:
            has_more = False
        x += 1
        df = pd.DataFrame.from_dict(response)
        df.to_csv(r'answers.csv',index="origin",mode="a",header=False)
        
def get_tags(from_date,to_date,order):
    has_more = True
    
    utc_from_date=datetime.datetime(int(from_date[0:4]),int(from_date[5:7]),int(from_date[8:10]))
    utc_from_date=(((int(utc_from_date.strftime("%Y"))-int(1970))*365)+int(utc_from_date.strftime("%d")))*24*60*60
    
    utc_to_date=datetime.datetime(int(to_date[0:4]),int(to_date[5:7]),int(to_date[8:10]))
    utc_to_date=(((int(utc_to_date.strftime("%Y"))-int(1970))*365)+int(utc_to_date.strftime("%d")))*24*60*60
    
    while has_more:
        x = 1
        url="https://api.stackexchange.com/2.3/tags?page=%s&pagesize=100&fromdate=1523059200&order=desc&sort=name&site=stackoverflow&key=uvLkWOoIdmLvryg2A2L)LQ((" % (str(x),utc_from_date,utc_to_date,order)
        response = requests.get(url)
        response=response.json()
        has_more = response["has_more"]
        if has_more == True:
            has_more = True
        else:
            has_more = False
        x += 1
        df = pd.DataFrame.from_dict(response)
        df.to_csv(r'tags.csv',index="origin",mode="a",header=False)