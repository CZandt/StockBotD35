#Trade

#List of Trades that are qued
#List of Trades that have been executed

#Methods
    #Add a trade to the Que
    #Remove a trade from the que
    #Display the qued trades
    #Display Trade History
import Trade
    

class TradeQue :
    def __init__(self):
        self.tradeHistory = [] #Creates a list to store the history of trades
        self.tradeQue = [] #creates a list to store the trades that are qued
        self.tradeID = 0
        self.tradesToExecute = []

    def addTradetoQue(self, tradeTicker, tradeDate, tradePrice, tradeShares, tradeAction, tradeAlg, lastHundredGain): #creates a trade object and adds it to the trade que list
        self.tradeQue.append(Trade.Trade(tradeTicker, tradeDate, tradePrice, tradeShares, tradeAction, tradeAlg,lastHundredGain,self.tradeID))
        self.tradeID += 1
        
    def addTradetoHistory(self, tradeID): #Switches a trade object from the que list to the history list
        try:
            for i in range(len(self.tradeQue)) : #goes through each trade in the que
                if (tradeID == self.tradeQue[i].returnTradeID()): #Checks if the trade in the que is the trade with the ID
                    self.tradeHistory.append(self.tradeQue[i]) #appends the specified trade to the trade history

                    del self.tradeQue[i] # deletes the trade from the que after it has been added to history

        except:
            print("ERROR TRANSFERRING TRADE FROM QUE TO HISTORY") #in case something goes wrong

    def displayTradeQue(self) :
        for i in range(len(self.tradeQue)) : #goes through each thing in the list
            print()
            print('Ticker:', self.tradeQue[i].returnTicker())
            print("\t Action:", self.tradeQue[i].returnTradeAction())
            print("\t Alg: " + self.tradeQue[i].returnTradeAlg())
            print("\t Date:", self.tradeQue[i].returnDate())
            print("\t Price: $" + str(self.tradeQue[i].returnPrice()))
            print("\t Shares:", self.tradeQue[i].returnShares())
            print("\t Trade ID:", self.tradeQue[i].returnTradeID())
            print("\t Last 100 Day Returns: " + str(self.tradeQue[i].returnLastHundredGain()) + '%')
            print()
        print("--- END OF TRADE QUE ---")

    def displayTradeHisotry(self) :
        for i in range(len(self.tradeHistory)) :
            print(str(i + 1) + ". Ticker:", self.tradeHistory[i].returnTicker())
            print("\t Date:", self.tradeHistory[i].returnDate())
            print("\t Alg: " + self.tradeHistory[i].returnTradeAlg())
            print("\t Price: $" + str(self.tradeHistory[i].returnPrice()))
            print("\t Shares:", self.tradeHistory[i].returnShares())
            print()
            print('-------------------')
            print()

        print("--- END OF HISTORY ---")

    def addTradesToExecute(self, iDsToBeMoved):
        tempIdHold = []
        for i in range(len(iDsToBeMoved)): # goes through each ID
            for j in range(len(self.tradeQue)) : #Goes through each trade in the Que

                if self.tradeQue[j].returnTradeID() == iDsToBeMoved[i]: #checks if the trade in the Que has ID == to the ID in the list

                    self.tradesToExecute.append(self.tradeQue[j]) # If the IDs match then the trade gets moved into the execution list
                    tempIdHold.append(self.tradeQue[j].returnTradeID())
        
        try:
            for i in range(len(tempIdHold)) :
                for j in range(len(self.tradeQue)):

                    if tempIdHold[i] == self.tradeQue[j].returnTradeID():
                        del self.tradeQue[j]
        except:
            print("ERROR DELETING TRADE AFTER MOVE")


    def displayTradeExecution(self) :
        for i in range(len(self.tradesToExecute)) : #goes through each thing in the list
            print()
            print('Ticker:', self.tradesToExecute[i].returnTicker())
            print("\t Action:", self.tradesToExecute[i].returnTradeAction())
            print("\t Alg: " + self.tradesToExecute[i].returnTradeAlg())
            print("\t Date:", self.tradesToExecute[i].returnDate())
            print("\t Price: $" + str(self.tradesToExecute[i].returnPrice()))
            print("\t Shares:", self.tradesToExecute[i].returnShares())
            print("\t Trade ID:", self.tradesToExecute[i].returnTradeID())
            print("\t Last 100 Day Returns: " + str(self.tradesToExecute[i].returnLastHundredGain()) + '%')
            print()
        print("--- END OF TRADE QUE ---")

    def returnTradeExecution(self):
        return self.tradesToExecute


    




