# Daily Population Bot
# Follow on twitter @DailyPopulation
# By Logicmn

from datetime import datetime, timedelta
from random import randint
from time import sleep
from tweepy import OAuthHandler, API
from pprint import pprint
import requests
import re

consumer_key = ''                                                       # Input consumer key
consumer_secret = ''                                                    # Input secret consumer key
access_token = ''                                                       # Input access token
access_token_secret = ''                                                # Input secret access token

auth = OAuthHandler(consumer_key, consumer_secret)                      # Input Twitter app credentials
auth.set_access_token(access_token, access_token_secret)                # Initiate connection to Twitter bot
twitterBot = API(auth)

def main():
    while True:
        todayPop = worldPopulation()                                    # Define the current world population
        percent, popChange = populationChange(todayPop)                 # Find the percent change and population change from yesterday to today
        twitterBot.update_status('Currently there are {0} people on earth. That is a {1} increase since yesterday!'.format(todayPop, popChange))
        sleep(86400)                                                    # Pause for 24 hours

def worldPopulation():                                                  # Grab the worlds population in .json format by using a GET request
    x = requests.get('http://api.population.io/1.0/population/World/today-and-tomorrow/')
    world = x.json()
    worldPop = world['total_population']
    today = worldPop[0]
    todayPop = int(today['population'])                                 # Convert the population to an integer
    return todayPop

def populationChange(todayPop):
    yesterday = datetime.today() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    r = requests.get('http://api.population.io/1.0/population/World/{}/'.format(yesterday))
    result = r.json()
    lastPop = int(result['total_population']['population'])     
    percent = 100 * (1 - lastPop/float(todayPop))                              # Calculate the percent change
    popChange = todayPop - lastPop                                      # Calculate the population change
    print(lastPop, todayPop)
    print(percent, popChange)
    return(percent, popChange)

main()
