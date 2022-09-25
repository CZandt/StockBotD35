# final_project

# TO DO 
# MAKE A BETTER TRADE ID SEQUENCE WHICH INCLUDES A COMBINATION OF DATETIME,TICKER,AND,PRICE
#START INTEGRATING WITH TRADING API SO THAT IT CAN TRADE ON ITS OWN
# CREATE ALGORITHIMS FOR HIGH FREQUENCY TRADING (BETA)

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

tickers = ['SPY','DOCU', 'EXPD', 'TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMD', 'BB', 'SPOT','AMZN','LCID','SBUX','NKE','GOOG','EA','DIS','GE','LULU','PLUG','GME','AAL','NVR','SEB','MMM','ATVI','AFL','AME','T','BBY','COF','KO','CMCSA','COST','F','GM','GS','HON','JNJ','K','MAR','NFLX','QCOM','RTX','CRM','LUV','USB','V','YUM']  # lists out the tickers that the program uses
#['SPY','DOCU']
uPref = input("Print ever trade? (Y or N)")

theTradeQue = TradeQue.TradeQue()
today = date.today()
def saveResults(results):  # Function to save results to json file
    json.dump(results, open('MacintoshHD/Users/colehardy/Desktop/results.json','w'))   #LOCATION FOR FILES IS NOT WORKING


def meanReversionStrategy(price, ticker, uPref):  # Function that contains the meanReversionStrategy
    day = 0  # records what day it currently is for the program
    buys = 0  # records the number of buys
    rProfit = 0  # rolling profit over all trades
    buy = 0  # what the buy price is
    firstbuy = 0  # variable tp record the first buy price
    returnPer = 0  # records the return percentage for all trades
    sell = 0  # records the price to sell
    suggestion = []  # creates a list to store what the algorithim suggests doing today
    lastBuy = 0  # to store what day the last buy was
    lastSSSell = 0  # to store what day the lastSSSell was
    lastSell = 0  # to store what day the last sell was
    lastSSBuy = 0  # to store what day the last SSBuy was
    tolerence = []
    stoplosses = 0
    dayZeroValue = 0
    dayEndValue = 0
    printColor = 'white'

    if ticker == 'SPY' or 'EXPD':
        tolerence = [0.97, 1.03]
    else:
        tolerence = [0.95, 1.05]
    for current_price in price:  # for loop that loops through each price day by day

        if day >= 5:  # only starts buying and calculating averages after 5 days have passed

            Avg_price = (sum(price[day - 5:day]) / 5)  # average prive over the last 5 days

            if current_price < Avg_price * tolerence[0]:  # if the current price is under 95% of the average it moves into the buy if statements

                if buy == 0:  # if no buys have already been done.
                    current_price = round(current_price, 2)  # rounds current price to 2 decimals

                    buy = current_price  # sets buy price to the current price

                    if uPref == 'Y':
                        print('Buying at:', buy)  # prints out what price it is buying at

                    if buys == 0:  # if no buys have been recorded then it records what the price of the first buy was
                        firstbuy = buy  # records first buy
                        if uPref == 'Y':
                            print('First buy:', buy)  # prints out what the first buy is

                    buys += 1  # records that a buy has occured

                    lastBuy = day  # records the day of the last buy

                if sell != 0:  # if there is a sell saved for short selling it goes into this statement
                    tProfit = round(sell - current_price, 2)  # records the trade profit
                    if uPref == 'Y':
                        print('Short sell at:', current_price)  # records the price it sold the short at
                        print('Short sell profit:', tProfit)  # records the profit made off the trade

                    # rProfit += tProfit # adds the profit from the trade to the rolling profit total

                    sell = 0  # resets the sale price to 0 for the next round of short selling

                    lastSSSell = day  # records what day the last time this action was made



            elif current_price > Avg_price * tolerence[1]:  # if the price is above 105% of the average
                if buy != 0:
                    tProfit = current_price - buy  # calculates how much profit was earned on the trade
                    tProfit = round(tProfit, 2)  # rounds profit to 2 decimal places

                    rProfit += tProfit  # adds the trade profit to the rolling profit variable to keep track of all profits

                    if uPref == 'Y':
                        print('Selling at:', current_price)  # Prints what price it is being sold at
                        print('Trade profit:', tProfit)  # prints the trade profit
                    buy = 0  # resets the buy price back to 0

                    lastSell = day  # records the last time a sell action occurred

                if sell == 0:
                    sell = round(current_price, 2)
                    if uPref == 'Y':
                        print('Short sell buy at:', sell)
                    lastSSBuy = day  # records the last day that a short sell buy occured
            elif current_price <= buy * 0.93:
                tProfit = current_price - buy
                tProfit = round(tProfit, 2)

                #rProfit += tProfit
                if uPref == 'Y':
                    print('Short Selling at:', current_price)
                    print('Trade profit:', tProfit)
                stoplosses += 1
                buy = 0

        if (day == 0): # checks if the first day is the one being analyzed
            dayZeroValue = current_price #sets the day one price to the current price

        dayEndValue = current_price #keeps track of the final price used

        day += 1  # records that a day has passed

    lastOperation = [lastBuy, lastSSSell, lastSell,
                     lastSSBuy]  # puts all the days that a last operation occured into a list

    if max(lastOperation) == day - 1:  # if the max of last operation is equal to the current day (day-1 cause day still gets added at the end)
        if day - 1 == lastBuy:  # appends a buy sign to the suggestion list if a buy occured on the last day
            suggestion.append('Buy')
        if day - 1 == lastSSSell:  # appends a cash in the short sign to the suggestion list if a lastSSSell occured on the last day
            #suggestion.append('Cash in the Short')
            pass
        if day - 1 == lastSell:  # appends a sell suggestion to the suggestion list if a sell occured on the last day
            suggestion.append('Sell')
        if day - 1 == lastSSBuy:  # appends a buy the short sign to the suggestion list if a short buy occured on the last day
            pass
            #suggestion.append('Buy the Short')

    if buys != 0:
        returnPer = (rProfit / firstbuy) * 100  # calculates the return percentage over all the trades
        returnPer = round(returnPer, 2)  # rounds the return percentage to 2 decimal places
    rProfit = round(rProfit, 2)

    print('----------------------')
    print(f'{ticker} MR Total Profit: {rProfit}')  # displays  the total profit of all the trades
    print('Stoplosses Triggered:', stoplosses)
    print('First Buy:', firstbuy)  # prints what the price of the first buy was
    print(colored(f'{ticker} MR Percentage returns: {returnPer}%', 'blue', attrs=['bold']))  # prints what the total return percent


    if suggestion != []:  # if a suggestion had occured
        try:
            print('Today the strategy suggests to' + suggestion[0] + 'and', suggestion[1], ' @ $' + str(current_price))  # prints out what the suggestion is
        except:
            if suggestion[0] == 'Buy':
                printColor = 'green'
            elif suggestion[0] == 'Sell':
                printColor = 'red'
            else:
                printColor = 'blue'
            print(colored('Today the strategy suggests to ' + suggestion[0] + ' @ $' + str(current_price), printColor, attrs=['bold']))  # if only one suggestion is given then this will work so it isnt gonna crash
    else:
        print('Today the strategy suggests to do nothing')  # if no suggestion it prints that it suggests to do nothing


    print('Hold Return ', round(dayEndValue - dayZeroValue,2), 'Percent: ', round(((dayEndValue / dayZeroValue) - 1) * 100,2),'%' )
    if (returnPer > ((dayEndValue / dayZeroValue) - 1) * 100) :
        print(colored('OUTPERFORMS HOLD', 'red', attrs=['bold']))
    print('----------------------')

    return returnPer, rProfit, suggestion, current_price  # returns the return percentage and Rolling profit and the suggestion out of the function


def simpleMovingAverageStrategy(price, ticker, uPref):  # defines the simpleMovingAverageStrategy function

    day = 0  # records what day it currently is for the program
    buys = 0  # records the number of buys
    rProfit = 0  # rolling profit over all trades
    buy = 0  # what the buy price is
    firstbuy = 0  # records what teh first buy price is
    returnPer = 0  # records the return percentage
    sell = 0  # records the sell price for short selling
    suggestion = []  # records the suggestions in a list to keep track of then
    lastBuy = 0  # records what day the last buy was
    lastSSSell = 0  # records what the last shortsell sell was
    lastSell = 0  # records what day the last sell was
    lastSSBuy = 0  # records what day the last short sell buy was
    stoplosses = 0
    dayZeroValue = 0
    dayEndValue = 0
    printColor = 'white'

    for current_price in price:  # for each price in the price list it goes through this equation

        if day >= 10:  # if the day is over day 10 it moves into the buying and selling because it is a 10 day moving average

            Avg_price = (sum(price[day - 10:day]) / 10)  # calculates teh average price over the last 10 days

            if current_price < Avg_price:  # if the current price is less than the average price over the last ten days it goes into the buy if statemnt

                if buy == 0:  # if a buy has not been recorded then it goes into this if statement
                    current_price = round(current_price, 2)  # rounds current price to 2 decimals

                    buy = current_price  # sets buy price to the current price
                    if uPref == 'Y':
                        print('Buying at:', buy)  # prints out what price it is buying at

                    if buys == 0:  # if no buys have been recorded then it records what the price of the first buy was
                        firstbuy = buy  # records first buy
                        if uPref == 'Y':
                            print('First buy:', buy)  # prints out what the first buy is

                    buys += 1  # records that a buy has occured

                    lastBuy = day  # records the day of the last buy

                if sell != 0:  # if there is a sell recorded for short selling
                    tProfit = round(sell - current_price, 2)  # records what the profit was for the trade
                    if uPref == 'Y':
                        print('Short sell at:', current_price)  # prints what the price of the trade is
                        print('Short sell profit:', tProfit)  # prints the profit for the trade

                    #rProfit += tProfit  # adds the profit from the trade to rolling total

                    sell = 0  # resets the sale price to 0 for the next round of short selling

                    lastSSSell = day  # records the day of the lastSSSell

            elif current_price > Avg_price:  # if the sell conditions are met then it moves into the selling if statement

                if buy != 0:  # if a buy has been recorded it goes into this statment

                    tProfit = current_price - buy  # calculates how much profit was earned on the trade
                    tProfit = round(tProfit, 2)  # rounds profit to 2 decimal places

                    rProfit += tProfit  # adds the trade profit to the rolling profit variable to keep track of all profits

                    if uPref == 'Y':
                        print('Selling at:', current_price)  # Prints what price it is being sold at
                        print('Trade profit:', tProfit)  # prints the trade profit
                    buy = 0  # resets the buy price back to 0

                    lastSell = day  # records the day of the last sale

                if sell == 0:  # if there is not a sell recorded then it goes into this
                    sell = round(current_price, 2)  # records the price that it bought the short at
                    if uPref == 'Y':
                        print('Short sell buy at:', sell)  # prints out what price it bought the short at
                    lastSSBuy = day  # records the day that is the last time that it bought the short

                buy = 0  # sets the buy equal to 0 becuase we sold

            elif current_price <= buy * 0.93:
                tProfit = current_price - buy
                tProfit = round(tProfit, 2)

                #rProfit += tProfit REMOVES SHORT SELLING FROM OVERALL TOTAL
                if uPref == 'Y':
                    print('Short Selling at:', current_price)
                    print('Trade profit:', tProfit)
                stoplosses += 1
                buy = 0

        if (day == 0): # checks if the first day is the one being analyzed
            dayZeroValue = current_price #sets the day one price to the current price

        dayEndValue = current_price #keeps track of the final price used

        day += 1  # adds 1 to the day counter so it moves to the next day
    lastOperation = [lastBuy, lastSSSell, lastSell, lastSSBuy]
    if max(lastOperation) == day - 1:  # if the max of last operation is equal to the current day (day-1 cause day still gets added at the end)
        if day - 1 == lastBuy:  # appends a buy sign to the suggestion list if a buy occured on the last day
            suggestion.append('Buy')
        if day - 1 == lastSSSell:  # appends a cash in the short sign to the suggestion list if a lastSSSell occured on the last day
            pass
            #suggestion.append('Cash in the Short')
        if day - 1 == lastSell:  # appends a sell suggestion to the suggestion list if a sell occured on the last day
            suggestion.append('Sell')
        if day - 1 == lastSSBuy:  # appends a buy the short sign to the suggestion list if a short buy occured on the last day
            #suggestion.append('Buy the Short')
            pass

    returnPer = round((rProfit / firstbuy) * 100,2)  # calculates the percentage return over all trades and rounds it to 2 decimal places
    rProfit = round(rProfit, 2)  # rounds the rolling profit to 2 decimal places
    print('----------------------')
    print(f'{ticker} SMA Total Profit:', rProfit)  # displays  the total profit of all the trades
    print('First Buy:', firstbuy)  # prints what the price of the first buy was
    print(colored(f'{ticker} SMA Percentage returns: {returnPer}%', 'blue', attrs=['bold']))  # prints what the total return percent

    if suggestion != []:  # if a suggestion had occured
        try:
            print('Today the strategy suggests to' + suggestion[0] + 'and', suggestion[1], ' @ $' + str(current_price))  # prints out what the suggestion is
        except:
            if suggestion[0] == 'Buy':
                printColor = 'green'
            elif suggestion[0] == 'Sell':
                printColor = 'red'
            else:
                printColor = 'blue'
            print(colored('Today the strategy suggests to ' + suggestion[0] + ' @ $' + str(current_price), printColor, attrs=['bold']))  # if only one suggestion is given then this will work so it isnt gonna crash
    else:
        print('Today the strategy suggests to do nothing')  # if no suggestion it prints that it suggests to do nothing


    print('Hold Return ', round(dayEndValue - dayZeroValue,2), 'Percent: ', round(((dayEndValue / dayZeroValue) - 1) * 100,2),'%' )
    if (returnPer > ((dayEndValue / dayZeroValue) - 1) * 100) :
        print(colored('OUTPERFORMS HOLD', 'red', attrs=['bold']))
    print('----------------------')

    return returnPer, rProfit, suggestion, current_price  # returns the return percentage and Rolling profit and the suggestion out of the function


def bollingerBondsStrategy(price, ticker, uPref): #Defines the bollingerBonds trading strategy function (once a day price variation changes)
    day = 0  # records what day it currently is for the program
    buys = 0  # records the number of buys
    rProfit = 0  # rolling profit over all trades
    buy = 0  # what the buy price is
    firstbuy = 0  # records what teh first buy price is
    returnPer = 0  # records the return percentage
    sell = 0  # records the sell price for short selling
    suggestion = []  # records the suggestions in a list to keep track of then
    lastBuy = 0  # records what day the last buy was
    lastSSSell = 0  # records what the last shortsell sell was
    lastSell = 0  # records what day the last sell was
    lastSSBuy = 0  # records what day the last short sell buy was
    stoplosses = 0
    dayZeroValue = 0
    dayEndValue = 0
    printColor = 'white'

    for current_price in price:  # for each price in the price list it goes through this equation

        if day >= 7:  # if the day is over day 10 it moves into the buying and selling because it is a 10 day moving average

            Avg_price = (sum(price[day - 7:day]) / 7)  # calculates teh average price over the last 10 days
            sdPrice = stat.stdev(price[day - 7:day])

            if current_price < (Avg_price - (
                    sdPrice * 1.5)):  # if the current price is less than the average price over the last ten days it goes into the buy if statemnt

                if buy == 0:
                    current_price = round(current_price, 2)  # rounds current price to 2 decimals

                    buy = current_price  # sets buy price to the current price
                    if uPref == 'Y':
                        print('Buying at:', buy)  # prints out what price it is buying at

                    if buys == 0:  # if no buys have been recorded then it records what the price of the first buy was
                        firstbuy = buy  # records first buy
                        if uPref == 'Y':
                            print('First buy:', buy)  # prints out what the first buy is

                    buys += 1  # records that a buy has occured

                    lastBuy = day  # records the day of the last buy

                if sell != 0:  # if no sell has been recorded then it goes into the short sell sell statment
                    tProfit = round(sell - current_price, 2)  # calculates the profit for the trade
                    if uPref == 'Y':
                        print('Short sell at:', current_price)  # prints what price the action is taken at
                        print('Short sell profit:', tProfit)  # Prints out the profit for the trade

                    #rProfit += tProfit  # adds the profit to the rolling total of profit

                    sell = 0  # resets the sale price to 0 for the next round of short selling

                    lastSSSell = day  # records the last day that the action occured
            elif current_price > (Avg_price + (
                    sdPrice * 1.5)):  # if the sell conditions are met then it moves into the selling if statement
                if buy != 0:
                    tProfit = current_price - buy  # calculates how much profit was earned on the trade
                    tProfit = round(tProfit, 2)  # rounds profit to 2 decimal places

                    rProfit += tProfit  # adds the trade profit to the rolling profit variable to keep track of all profits
                    if uPref == 'Y':
                        print('Selling at:', current_price)  # Prints what price it is being sold at
                        print('Trade profit:', tProfit)  # prints the trade profit
                    buy = 0  # resets the buy price back to 0

                    lastSell = day  # records the last day that a buy occured

                if sell == 0:
                    sell = round(current_price, 2)  # records what price the short sell buy occured at
                    if uPref == 'Y':
                        print('Short sell buy at:', sell)  # Prints out what price the short buy occured
                    lastSSBuy = day  # records the last day the action occured

                buy = 0  # sets the buy equal to 0 becuase we sold

            elif current_price <= buy * 0.93:
                tProfit = current_price - buy
                tProfit = round(tProfit, 2)

                #rProfit += tProfit
                if uPref == 'Y':
                    print('Short Selling at:', current_price)
                    print('Trade profit:', tProfit)
                stoplosses += 1
                buy = 0
                lastSell = day

        if (day == 0): # checks if the first day is the one being analyzed
            dayZeroValue = current_price #sets the day one price to the current price

        dayEndValue = current_price #keeps track of the final price used

        day += 1  # adds 1 to the day counter so it moves to the next day

    lastOperation = [lastBuy, lastSSSell, lastSell, lastSSBuy]
    if max(lastOperation) == day - 1:  # if the max of last operation is equal to the current day (day-1 cause day still gets added at the end)
        if day - 1 == lastBuy:  # appends a buy sign to the suggestion list if a buy occured on the last day
            suggestion.append('Buy')
            # if day-1 == lastSSSell: #appends a cash in the short sign to the suggestion list if a lastSSSell occured on the last day
            # suggestion.append('Cash in the Short')
        if day - 1 == lastSell:  # appends a sell suggestion to the suggestion list if a sell occured on the last day
            suggestion.append('Sell')
        # if day-1 == lastSSBuy: # appends a buy the short sign to the suggestion list if a short buy occured on the last day
        # suggestion.append('Buy the Short')

    returnPer = round((rProfit / firstbuy) * 100,
                      2)  # calculates the percentage return over all trades and rounds it to 2 decimal places
    rProfit = round(rProfit, 2)  # rounds the rolling profit to 2 decimal places
    print('----------------------')
    print(f'{ticker} Bollinger Bonds Total Profit:', rProfit)  # displays  the total profit of all the trades
    print('First Buy:', firstbuy)  # prints what the price of the first buy was
    print(colored(f'{ticker} Bollinger Bonds Percentage returns: {returnPer}%', 'blue', attrs=['bold']))  # prints what the total return percent


    if suggestion != []:  # if a suggestion had occured
        try:
            print('Today the strategy suggests to' + suggestion[0] + 'and', suggestion[1], ' @ $' + str(current_price))  # prints out what the suggestion is
        except:
            if suggestion[0] == 'Buy':
                printColor = 'green'
            elif suggestion[0] == 'Sell':
                printColor = 'red'
            else:
                printColor = 'blue'
            print(colored('Today the strategy suggests to ' + suggestion[0] + ' @ $' + str(current_price), printColor, attrs=['bold']))  # if only one suggestion is given then this will work so it isnt gonna crash
    else:
        print('Today the strategy suggests to do nothing')  # if no suggestion it prints that it suggests to do nothing


    print('Stoplosses triggered:', stoplosses)
    print('Hold Return ', round(dayEndValue - dayZeroValue,2), 'Percent: ', round(((dayEndValue / dayZeroValue) - 1) * 100,2),'%' )
    if (returnPer > ((dayEndValue / dayZeroValue) - 1) * 100) :
        print(colored('OUTPERFORMS HOLD', 'red', attrs=['bold']))
    print('----------------------')

    return returnPer, rProfit, suggestion, current_price  # returns the return percentage and Rolling profit and the suggestion out of the function

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

    meanResult = meanReversionStrategy(prices, ticker, uPref)  # save the results from the MRstrat and runs it
    smaResult = simpleMovingAverageStrategy(prices, ticker, uPref)  # saves the results from the SMAstrat and runs it
    bbResult = bollingerBondsStrategy(prices, ticker, uPref)  # saves the results from the BBstrat and runs it
    

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
        theTradeQue.addTradetoQue(ticker,today.strftime("%m/%d/%y"), meanResult[3], 1, round((random() % 10000) * 10000, 0),meanResult[2],"Mean Reversion")

    if smaResult[2] == ['Buy'] or smaResult[2] == ['Sell']: #for SMA
        theTradeQue.addTradetoQue(ticker, today.strftime("%m/%d/%y"), smaResult[3], 1, round((random() % 10000) * 10000, 0), smaResult[2], "Simple Moving Average")
    
    if bbResult[2] == ['Buy'] or bbResult[2] == ['Sell']: # for BB
        theTradeQue.addTradetoQue(ticker, today.strftime("%m/%d/%y"), bbResult[3], 1,round((random() % 10000) * 10000, 0),bbResult[2], "Bollinger Bonds")


    time.sleep(12) # waits 
  #saveResults(results) #calls the results function and saves the results dictionary as a json file

theTradeQue.displayTradeQue() #displays the trades that are in the que to be placed