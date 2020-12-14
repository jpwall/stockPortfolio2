import time
import urllib.parse, urllib.request, urllib.error, json
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
        mult = self.multiplier()
        return "{} \x1b[0m{}{:^8}\x1b[0m {:^7} {:^12} {:^12} {:^12.2f} {:^12.2f} {}{}%\x1b[0m".format(
            self.id, self.symbolColor(), self.symbol, 
            str(int(mult) * int(self.shares)), 
            self.buy_price, 
            self.current_price,
            abs(self.expense()),
            self.profit(),
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
        quote = 0.0
        if self.symbol != 'BTC' and self.symbol != 'btc':
            url = "https://old.nasdaq.com/symbol/{}/real-time".format(self.symbol)
            page = session.get(url)
            quote = page.html.find("div#qwidget_lastsale.qwidget-dollar")[0].text[1:]
        else:
            btc_str = urllib.request.urlopen("https://api.coindesk.com/v1/bpi/currentprice.json")
            btc_data = json.load(btc_str)
            quote = btc_data["bpi"]["USD"]["rate_float"]
        self.current_price = float(quote)
        return float(quote)
    
    def roi(self):
        roi_ret = (float(self.profit()) / float(abs(self.expense()))) * 100
        return round(roi_ret, 3)
    
    def expense(self):
        return (float(self.buy_price) * int(self.multiplier()) * float(self.shares))
    
    def profit(self):
        return (float(self.current_price) * int(self.multiplier()) * float(self.shares)) - float(self.expense())
    
    def sell(self):
        self.sell_price = self.current_price
        self.sold = True
    
    def multiplier(self):
        if self.short == True:
            return -1
        else:
            return 1