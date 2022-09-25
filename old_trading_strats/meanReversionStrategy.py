

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

                rProfit += tProfit
                if uPref == 'Y':
                    print('STOP LOSS SELL at:', current_price)
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