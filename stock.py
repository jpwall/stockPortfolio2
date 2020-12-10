import time
from requests_html import HTMLSession
session = HTMLSession()

class Stock:
    """Stock object for bookkeeping of holdings"""

    def __init__(self, symbol, shares=1, short=False, buy_price=None, sell_price=None):
        #self.current_price = self.refresh()
        self.id = int(time.time())
        self.current_price = 0.0
        self.symbol = symbol.upper()
        self.refresh()
        self.shares = shares
        if buy_price != None:
            self.buy_price = buy_price
        else:
            self.buy_price = self.current_price
        self.sell_price = sell_price
        self.short = short
        if sell_price is None:
            self.sold = False
        else:
            self.sold = True
    
    def __lt__(self, other):
        return self.roi() < other.roi()
    
    def __str__(self):
        return "{} \x1b[0m{}{:^8}\x1b[0m {:^7} {:^9} {:^9} {:^12.2f} {:^12.2f} {}{}%\x1b[0m".format(
            self.id, self.symbolColor(), self.symbol, 
            self.shares, 
            self.buy_price, 
            self.current_price,
            int(self.shares) * float(self.buy_price),#expense,
            (int(self.shares) * float(self.current_price)) - (int(self.shares) * float(self.buy_price)),#profit,
            self.roiColor(), self.roi()
            )
    
    def symbolColor(self):
        if self.sold:
            return "\x1b[0;34m"
        else:
            return "\x1b[0;35m"
    
    def roiColor(self):
        current_roi = self.roi()
        if current_roi <= 0.0:
            return "\x1b[0;31m" #red
        elif current_roi <= 6.0:
            return "\x1b[0;33m" #yellow
        else:
            return "\x1b[0;32m" #green
    
    def refresh(self):
        if self.symbol != 'BTC':
            url = "https://old.nasdaq.com/symbol/{}/real-time".format(self.symbol)
            page = session.get(url)
            quote = page.html.find("div#qwidget_lastsale.qwidget-dollar")[0].text[1:]
            self.current_price = quote
            return quote
        else:
            # TODO: Add coindesk api for price scraping
            self.current_price = 0.0
            return 0.0
    
    def roi(self):
        recent = 0
        if self.sold:
            recent = float(self.sell_price)
        else:
            recent = float(self.current_price)
        profit = (recent - float(self.buy_price)) * int(self.shares)
        expense = float(self.buy_price) * int(self.shares)
        roi_ret = (profit / expense) * 100
        return round(roi_ret, 3)
    
    def expense(self):
        return float(self.buy_price) * int(self.shares)
    
    def profit(self):
        return (float(self.current_price) * int(self.shares)) - self.expense()
    
    def sell(self):
        self.sell_price = self.current_price
        self.sold = True