

import TradeQue

def tradeMenu() :
    print('OPTIONS')
    print('\t 1. PRINT TRADE SUGGESTIONS')
    print('\t 2. SELECT TRADES TO BE EXECUTED')
    print('\t 3. PRINT TRADES QUED FOR EXECUTION')
    print('\t 4. EXECUTE TRADES')
    print('\t 5. PRINT TRADE HISTORY')
    print('\t 6. QUIT')
    print()

def printTradeSuggestions(theTradeQue) :
    theTradeQue.displayTradeQue()

def selectTradesToExecute(theTradeQue) :
    theTradeQue.displayTradeQue()
    key = 0
    iDsToBeMoved = []
    tempIdHold = 0
    while key == 0:
        tempIdHold = int(input('Input TradeID for trade to be executed: '))
        iDsToBeMoved.append(tempIdHold)
        print()
        key = int(input('ENTER 0 TO ADD ANOTHER // ENTER 1 TO QUIT: '))
        print()

        theTradeQue.addTradesToExecute(iDsToBeMoved)

    #try:
        #theTradeQue.addTradesToExecute(iDsToBeMoved)
    #except:
        #print()
        #print('ERROR TRANSFERRING TRADES TO EXECUTION')
    
def printTradesToExecute(theTradeQue) :
    theTradeQue.displayTradeExecution()

def executeTrades(theTradeQue):
    print('PLACEHOLDER FOR EXECUTING TRADES')
    print('PLACEHOLDER FOR EXECUTING TRADES')

def printTradeHistory(theTradeQue):
    print('PLACEHOLDER NEEDS RESTRUCTURE OF TRADE HISTORY OBJECT')






    
