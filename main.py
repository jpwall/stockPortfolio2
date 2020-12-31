import sys
import pickle
import time
from stock import Stock

# TODO: arg parsing, list sorting
symbols = ["tsla", "amd", "intc", "ibm"]
holdings = []

# WRITE
def writeHolding():
    with open('portfolio.obj', 'wb') as w:
        pickle.dump(holdings, w)

def readHolding(suppress=False):
    with open('portfolio.obj', 'rb') as r:
        try:
            loaded = pickle.load(r)
            for stock in loaded:
                holdings.append(stock)
        except EOFError as e:
            if not suppress:
                print("Please buy a stock with 'b' argument before viewing portfolio. Further information through 'help'.")
                print("Pickle error: " + str(e))
    if not suppress:
        print("{:^10} \x1b[0m{}{:^8}\x1b[0m {:^7} {:^12} {:^12} {:^12} {:^12} {}{}%\x1b[0m".format("id", "", "ticker", "shares", "buy", "curr", "exp", "profit", "", "ROI"))

def main():
    if len(sys.argv) == 1:
        readHolding()
        for stock in holdings:
            if stock.sold != True:
                print(stock)
    
    elif sys.argv[1] == "help":
        print("HELP TODO")
    
    elif sys.argv[1] == "u":
        readHolding()
        for stock in holdings:
            if stock.sold != True:
                stock.refresh()
                print(stock)
        writeHolding()
    
    elif sys.argv[1] == "ub":
        readHolding()
        for stock in holdings:
            if stock.sold != True and stock.symbol.lower() == 'btc':
                stock.refresh()
                print(stock)
        writeHolding()

    elif sys.argv[1] == "all":
        readHolding()
        for stock in holdings:
            print(stock)
    
    elif sys.argv[1] == "sold":
        readHolding()
        for stock in holdings:
            if stock.sold == True:
                print(stock)
    
    elif sys.argv[1] == "stats":
        readHolding(suppress=True)
        h_expense = 0.00
        h_profit = 0.00
        s_expense = 0.00
        s_profit = 0.00
        for stock in holdings:
            if stock.sold:
                s_expense = s_expense + float(abs(stock.expense()))
                s_profit = s_profit + stock.profit()
            else:
                h_expense = h_expense + stock.expense()
                h_profit = h_profit + stock.profit()
        p_expense = h_expense + s_expense
        p_profit = h_profit + s_profit
        print("{:^38}".format("portfolio"))
        if p_expense == 0 or p_profit == 0:
            print("{:^38}".format("no data"))
        else:
            print("{:15.2f}{:^15.2f}{:>7.5f}%".format(p_expense, p_profit, 100 * float(p_profit / p_expense)))
        print("{:^38}".format("holding"))
        if h_expense == 0 or h_profit == 0:
            print("{:^38}".format("no data"))
        else:
            print("{:15.2f}{:^15.2f}{:>7.5f}%".format(h_expense, h_profit, 100 * float(h_profit / h_expense)))
        print("{:^38}".format("sold"))
        if s_expense == 0 or s_profit == 0:
            print("{:^38}".format("no data"))
        else:
            print("{:15.2f}{:^15.2f}{:>7.5f}%".format(s_expense, s_profit, 100 * float(s_profit / s_expense)))

    
    elif sys.argv[1] == "quote":
        tmp = Stock(symbol=sys.argv[2])
        print("{0:.2f}".format(tmp.current_price))
    
    elif sys.argv[1] == "b":
        readHolding(suppress=True)
        buy = Stock(symbol=sys.argv[2], shares=sys.argv[3])
        holdings.append(buy)
        writeHolding()
    
    elif sys.argv[1] == "short":
        readHolding(suppress=True)
        short = Stock(symbol=sys.argv[2], shares=sys.argv[3], short=True)
        holdings.append(short)
        writeHolding()
    
    elif sys.argv[1] == "s":
        readHolding()
        for stock in holdings:
            if stock.id == int(sys.argv[2]):
                stock.refresh()
                stock.sell()
                break
        writeHolding()
    
    elif sys.argv[1] == "oh":
        readHolding()
        holdings.sort(reverse=True)
        for stock in holdings:
            if not stock.sold:
                print(stock)
    
    else:
        print("Unknown argument! Please use 'help' for more options.")

main()