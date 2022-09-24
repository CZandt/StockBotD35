# Trade Class
    # Est. Price for Trade
    # Date of Trade
    # Ticker for the trade
    # Amount that is too be bought (IN SHARES NOT $$$$)

#Intializers, Add, and returns? That is it?

class Trade:

    def __init__(self, tradeTicker, tradeDate, tradePrice, tradeShares, tradeID, tradeAction, tradeAlg) :
        self.tradeTicker = tradeTicker
        self.tradeDate = tradeDate
        self.tradePrice = tradePrice
        self.tradeShares = tradeShares
        self.tradeID = tradeID
        self.tradeAction = tradeAction
        self.tradeAlg = tradeAlg

    def returnTicker(self) :
        return self.tradeTicker

    def returnDate(self) :
        return self.tradeDate

    def returnPrice(self) :
        return self.tradePrice

    def returnShares(self) :
        return self.tradeShares

    def returnTradeID(self) :
        return self.tradeID
    
    def returnTradeAction(self) :
        if self.tradeAction == ['Buy']:
            self.tradeAction = 'Buy'
        if self.tradeAction == ['Sell']:
            self.tradeAction = 'Sell'
            
        return self.tradeAction

    def returnTradeAlg(self) :
        return self.tradeAlg
    
