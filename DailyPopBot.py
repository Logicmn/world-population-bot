# Daily Population Bot
# Follow on twitter @DailyPopulation
# By Logicmn

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
    i = True
    while i == True:
        todayPop = worldPopulation()                                    # Define the current world population
        percent, popChange = populationChange(todayPop)                 # Find the percent change and population change from yesterday to today
        appendPop(todayPop)                                             # Add the population to a log file of all the past world populations
        twitterBot.update_status('Currently there are {0} people on earth. That is a {1} increase since yesterday!'.format(todayPop, popChange))
        sleep(60)                                                    # Pause for 24 hours

def worldPopulation():                                                  # Grab the worlds population in .json format by using a GET request
    x = requests.get('http://api.population.io:80/1.0/population/World/today-and-tomorrow/')
    world = x.json()
    worldPop = world['total_population']
    today = worldPop[0]
    todayPop = int(today['population'])                                 # Convert the population to an integer
    return todayPop

def appendPop(todayPop):
    with open("log.txt", "a") as logfile:
        logfile.write("\n{0}".format(str(todayPop)))                    # Log every population

def populationChange(todayPop):
    with open('log.txt', "rb") as logfile:
        logfile.seek(-20, 2)  # 2 means "from the end of the file"
        lastLine = logfile.readlines()[-1]
        lastPop = int("".join(map(chr, lastLine)))
        percent = 100 * (1 - lastPop/todayPop)                          # Calculate the percent change
        popChange = todayPop - lastPop                                  # Calculate the population change
        print(lastPop, todayPop)
        print(percent, popChange)
        return(percent, popChange)

main()
