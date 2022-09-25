# final_project

# TO DO 
# MAKE A BETTER TRADE ID SEQUENCE WHICH INCLUDES A COMBINATION OF DATETIME,TICKER,AND,PRICE
#PUT EACH ALG IN ITS OWN PYTHON FILE TO CLEAN UP FILE
#START INTEGRATING WITH TRADING API SO THAT IT CAN TRADE ON ITS OWN
# CREATE ALGORITHIMS FOR HIGH FREQUENCY TRADING (BETA)
# ADD A 4th ALG THAT SIMILAR TO THE MAGI WILL ONLY BUY/SELL IF 2/3 or 3/3 of the other algs agree with each other

from cgi import test
import json
from operator import attrgetter
from turtle import color  # imports the json module
import requests  # imports requests
import statistics as stat  # imports stat module for math calculations
import os  # imports the OS module
import time  # imports the time module so that alphavantage wont throw a fit
from termcolor import colored #imports termcolor for the text
import TradeQue #imports the tradeQue class
from datetime import date
from random import random
import meanReversion
import simpleMovingAverage
import bollingerBonds
import magi

#tickers = ['SPY','DOCU', 'EXPD', 'TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'BB', 'SPOT','AMZN','LCID','SBUX','NKE','GOOG','EA','DIS','GE','LULU','PLUG','GME','AAL','NVR','SEB','MMM','ATVI','AFL','AME','T','BBY','COF','KO','CMCSA','COST','F','GM','GS','HON','JNJ','K','MAR','NFLX','QCOM','RTX','CRM','LUV','USB','V','YUM']  # lists out the tickers that the program uses
tickers = ['SPY','DOCU','NFLX','PLUG','RTX','GME']

#tickers = ['UK','SBEV','CASI','TQQQ','SQQQ','CCL']
# YOU INVESTED ON DOCU BB MAKE SURE TO CHECK DAILY!!!!

#tickers = ['SPY','EXPD','NVDA','AAPL','MSFT','AMZN']#['BB','PLUG','SPOT','NFLX','DOCU','RTX','AAL','GME','LULU'] #ALL THESE SHOW POTENTIAL FOR REAL WORLD IMPLEMENTATION


uPref = input("Print ever trade? (Y or N)")

theTradeQue = TradeQue.TradeQue()
today = date.today()
def saveResults(results):  # Function to save results to json file
    json.dump(results, open('MacintoshHD/Users/colehardy/Desktop/results.json','w'))   #LOCATION FOR FILES IS NOT WORKING


results = {}  # creates a directory for the results of the function

for ticker in tickers:  # for each ticker in the ticker list it does this
    # Goes through each ticker and adds it to the API in a formatted string format to pull new data for each ticker
    url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey=JJI3NVB2R98E5ILV')  # URl that pulls the data for the ticker
    request = requests.get(url)  # saves the json from the request as request

    cDictionary = json.loads(request.text)  # loads the json into a dictionary

    key1 = "Time Series (Daily)"  # saves the first key in the dictionary
    # need all dates
    key2 = "4. close"  # saves the second static key in the dictionary

    prices = []  # creates a list for the prices of the stock

    for date in cDictionary[key1]:  # for each date in the dictionary it goes through this
        price = float(cDictionary[key1][date][key2])  # grabs the price and converts it to a float

        prices.append(price)  # adds the price to the list

    prices.reverse()

    # testindicator = (stat.stdev(prices) / (sum(prices)/len(prices)))

    # stockdata = open('/home/ubuntu/environment/Personal_Projects/data/' + ticker + '_data.csv', 'w') #creates a .csv file with the prices used

    # for date in cDictionary[key1]: # for each date it does this in the CSV
    # stockdata.write(date + ',' + cDictionary[key1][date][key2] + '\n' ) # this is supposed to save the CSV to the folder data but it is being funky

    meanResult = meanReversion.meanReversionStrategy(prices, ticker, uPref)  # save the results from the MRstrat and runs it
    smaResult = simpleMovingAverage.simpleMovingAverageStrategy(prices, ticker, uPref)  # saves the results from the SMAstrat and runs it
    bbResult = bollingerBonds.bollingerBondsStrategy(prices, ticker, uPref)  # saves the results from the BBstrat and runs it
    #magi33Result = magi.magiTrading33(prices, ticker, uPref) #saves the results from the MAGI33 and runs it
    #magi23Result = magi.magiTrading23(prices, ticker, uPref) #saves the results from the MAGI23 trading strat and runs it
    

    results[f'{ticker}_mr_profit'] = meanResult[1]  # stores the mean reversion profits in the dictionary

    results[f'{ticker}_mr_returns'] = meanResult[0]  # stores the mean reversion returns in the dictionary

    results[f'{ticker}_mr_suggestion'] = meanResult[2]  # stores the suggested action for the mean reversion in the dictionary

    results[f'{ticker}_sma_suggestion'] = smaResult[2]  # stores the suggested action for the simple moving average in the dictionary

    results[f'{ticker}_sma_profit'] = smaResult[1]  # stores the simple moving average profits in the dictionary

    results[f'{ticker}_sma_returns'] = smaResult[0]  # stores the simple moving average returns in the dictionary

    results[f'{ticker}_bb_profit'] = bbResult[0]  # stores the bollinger bonds profit in the dictionary

    results[f'{ticker}_bb_returns'] = bbResult[1]  # stores the bollinger bonds resturns in the dictionary

    results[f'{ticker}_bb_suggestion'] = bbResult[2]  # stores the bollinger bonds suggested action in the dictionary

    #CREATES A CLASS FOR A TRADE AND ADDS IT TO QUE IF IT A BUY OR SELL
    if meanResult[2] == ['Buy'] or meanResult[2] == ['Sell']: #creates an object in the trade que to represent a trade that is to be placed
        theTradeQue.addTradetoQue(ticker,today.strftime("%m/%d/%y"), meanResult[3], 1,meanResult[2],"Mean Reversion",meanResult[0])

    if smaResult[2] == ['Buy'] or smaResult[2] == ['Sell']: #for SMA
        theTradeQue.addTradetoQue(ticker, today.strftime("%m/%d/%y"), smaResult[3], 1, smaResult[2], "Simple Moving Average",smaResult[0])
    
    if bbResult[2] == ['Buy'] or bbResult[2] == ['Sell']: # for BB
        theTradeQue.addTradetoQue(ticker, today.strftime("%m/%d/%y"), bbResult[3], 1,bbResult[2], "Bollinger Bonds",bbResult[0])

    #if magi33Result[2] == ['Buy'] or magi33Result == ['Sell']: #for MAGI33
        #theTradeQue.addTradetoQue(ticker,today.strftime("%m/%d/%y"), magi33Result[3],1, 312324, magi33Result[2],"MAGI 33", magi33Result[1])

    #if magi23Result[2] == ['Buy'] or magi23Result == ['Sell']: #for MAGI23
        #theTradeQue.addTradetoQue(ticker,today.strftime("%m/%d/%y"), magi23Result[3],1, 312324, magi23Result[2],"MAGI 23", magi23Result[1])



    time.sleep(12) # waits 
  #saveResults(results) #calls the results function and saves the results dictionary as a json file

theTradeQue.displayTradeQue() #displays the trades that are in the que to be placed