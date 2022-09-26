from cgi import test
from operator import attrgetter
from turtle import color  # imports the json module
import statistics as stat  # imports stat module for math calculations
from termcolor import colored #imports termcolor for the text
from datetime import date
from random import random

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

                buy = 0  # sets the buy equal to 0 becuase we sold

            elif current_price <= buy * 0.93:
                tProfit = current_price - buy
                tProfit = round(tProfit, 2)

                rProfit += tProfit
                if uPref == 'Y':
                    print('STOP LOSS SELLING AT:', current_price)
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

        if day - 1 == lastSell:  # appends a sell suggestion to the suggestion list if a sell occured on the last day
            suggestion.append('Sell')


    returnPer = round((rProfit / firstbuy) * 100, 2)  # calculates the percentage return over all trades and rounds it to 2 decimal places
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