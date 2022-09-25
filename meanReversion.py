# Rewriting the mean Reversion Stratedgy as its own file
from cgi import test
from operator import attrgetter
from turtle import color  # imports the json module
import statistics as stat  # imports stat module for math calculations
from termcolor import colored #imports termcolor for the text
from datetime import date
from random import random

def meanReversionStrategy(price, ticker, uPref) :
    day = 0
    buys = 0
    rProfit = 0
    buy = 0
    firstBuy = 0
    returnPer = 0
    sell = 0
    suggestion = []
    lastBuy = 0
    lastSell = 0
    tolerence = []
    stopLosses = 0
    dayZeroValue = 0
    dayEndValue = 0
    printColor = 'white'

    #SETS THE TOLERNECE FROM THE MEAN FOR THE STRAT
    if ticker == 'SPY' or 'EXPD' :
        tolerence = [0.97, 1.03]
    else:
        tolerence = [0.95, 1.05]

    for current_price in price:
        
        if day >= 5 : #Uses a 5 day moving average so it has to start calculating on the 5th day

            avg_Price = (sum(price[day - 5 : day]) / 5) #calculates the 5 day mobing average

            if current_price < avg_Price * tolerence[0]: # if the current price is under the 95% threshold from the average it moves into the buy statments

                if buy == 0: #if no buy is currently happenening
                    current_price = round(current_price, 2)

                    buy = current_price #Executes a buy at the price

                    if uPref == 'Y':
                        print('Buying at:', buy)
                    
                    if buys == 0: # If no previous buy has occured it records the buy as the first buy
                        firstBuy = buy
                        if uPref == 'Y' :
                            print('First Buy:', buy)
                        
                    buys += 1

                    lastBuy = day #records the day that the lastBuy occured
                
            elif current_price > avg_Price * tolerence[1]: #checks if the current price is above the 105% average

                if buy != 0: #checks to see if a buy has been placed
                    tProfit = current_price - buy #calculates profit on the sell trade
                    tProfit = round(tProfit, 2)

                    rProfit += tProfit #adds profit from the trade to the rolling total

                    if uPref == 'Y':
                        print('Selling at:', current_price)
                        print('Trade Profit:', tProfit)
                    buy = 0 # Resets the buy variable 

                    lastSell = day # records the date that the last sell occured

            elif current_price <= buy * 0.93: #STOP LOSS CODE, avoids large losses
                tProfit = current_price - buy
                tProfit = round(tProfit, 2)

                rProfit += tProfit #adds the trade profit to the rolling total
                if uPref == 'Y':
                    print('STOP LOSS SELL AT:', current_price)
                    print('Trade Profit:', tProfit)
                
                stopLosses += 1 #records that a stop loss occured
                buy = 0 #resets the buy variable since you sold

        if (day == 0): #checks if the first day is being analyzed
            dayZeroValue = current_price #sets day one price to current price

        dayEndValue = current_price #keeps track of the final price used

        day += 1 #rise and shine a day has passed

    lastOperation = [lastBuy,lastSell]

    if max(lastOperation) == day - 1:
        if day - 1 == lastBuy:
            suggestion.append('Buy')
        if day - 1 == lastSell:
            suggestion.append('Sell')

    
    if buys != 0:
        returnPer = (rProfit / firstBuy) * 100 #calculates the percentage return over all trades
        returnPer = round(returnPer, 2) #rounds the return percentage to 2 decimal places

    rProfit = round(rProfit, 2)

    print('----------------------')
    print(f'{ticker} MR Total Profit: {rProfit}')  # displays  the total profit of all the trades
    print('Stoplosses Triggered:', stopLosses)
    print('First Buy:', firstBuy)  # prints what the price of the first buy was
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
