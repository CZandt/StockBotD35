# Trade Class
    # Est. Price for Trade
    # Date of Trade
    # Ticker for the trade
    # Amount that is too be bought (IN SHARES NOT $$$$)

#Intializers, Add, and returns? That is it?

class Trade: #class to represent a trade and all of its properties 

    def __init__(self, tradeTicker, tradeDate, tradePrice, tradeShares, tradeAction, tradeAlg,lastHundredGain,tradeID) :
        self.tradeTicker = tradeTicker #Stores the ticker for the trade
        self.tradeDate = tradeDate #Stores the date for the trade
        self.tradePrice = tradePrice #Stores the suggested price for the trade
        self.tradeShares = tradeShares #stores the amount of shares that are too be bought with the trade
        self.tradeAction = tradeAction #Records if the trade is a buy or sell trade
        self.tradeAlg = tradeAlg #Records the algorithim that is used for the trade
        self.lastHundredGain = lastHundredGain
        self.tradeID = tradeID

    def returnTicker(self) :
        return self.tradeTicker #Method to return the trade ticker

    def returnDate(self) :
        return self.tradeDate #Method to return the date that the trade is for 

    def returnPrice(self) :
        return self.tradePrice #Method to the return the price that the trade is supposed to be issued at 

    def returnShares(self) :
        return self.tradeShares #Method to return the amount shares that are supposed to be traded with the trade

    def returnTradeID(self) : #Method to return the TradeID for the trade
        return self.tradeID
    
    def returnTradeAction(self) : #Convers the funky list format for the trade action and then the normal type for the trade
        if self.tradeAction == ['Buy']:
            self.tradeAction = 'Buy'
        if self.tradeAction == ['Sell']:
            self.tradeAction = 'Sell'

        return self.tradeAction

    def returnTradeAlg(self) : #Returns the algorithim that was used to determine that the trade should be executed
        return self.tradeAlg
    
    def returnLastHundredGain(self):
        return self.lastHundredGain
    
