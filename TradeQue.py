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
        self.tradeHistory = []
        self.tradeQue = []

    def addTradetoQue(self, tradeTicker, tradeDate, tradePrice, tradeShares, tradeID, tradeAction, tradeAlg):
        self.tradeQue.append(Trade.Trade(tradeTicker, tradeDate, tradePrice, tradeShares, tradeID, tradeAction, tradeAlg))
    
    def addTradetoHistory(self, tradeID):
        try:
            for i in self.tradeQue : #goes through each trade in the que
                if (tradeID == self.tradeQue[i].returnTradeID()): #Checks if the trade in the que is the trade with the ID
                    self.tradeHistory.append(self.tradeQue[i]) #appends the specified trade to the trade history

                    del self.tradeQue[i] # deletes the trade from the que after it has been added to history

        except:
            print("ERROR TRANSFERRING TRADE FROM QUE TO HISTORY")

    def displayTradeQue(self) :
        for i in range(len(self.tradeQue)) :
            print('Ticker:', self.tradeQue[i].returnTicker())
            print("\t Action:", self.tradeQue[i].returnTradeAction())
            print("\t Date:", self.tradeQue[i].returnDate())
            print("\t Price: $" + str(self.tradeQue[i].returnPrice()))
            print("\t Shares:", self.tradeQue[i].returnShares())
            print()
            print('-----------------------')
            print()
        print(self.tradeQue)
        print("--- END OF TRADE QUE ---")

    def displayTradeHisotry(self) :
        for i in range(len(self.tradeHistory)) :
            print(str(i + 1) + ". Ticker:", self.tradeHistory[i].returnTicker())
            print("\t Date:", self.tradeHistory[i].returnDate())
            print("\t Alg: " + self.tradeHistory[i].returnTradeAlg())
            print("\t Price: $" + str(self.tradeHistory[i].returnPrice()))
            print("\t Shares:", self.tradeHistory[i].returnShares())
            print()

        print("--- END OF HISTORY ---")

    




