import requests
import json

def getAllTickers():
    url = "https://api.iextrading.com/1.0/ref-data/symbols"
    r = requests.get(url)
    all_stock_json_data = json.loads(r.text)
    for stock in all_stock_json_data:
        name = stock["name"]
        ticker = stock["symbol"]
        currentPrice = getCurrentPrice(ticker)
        sharesOutstanding = getOutStandingShare(ticker)
        marketCap = float(sharesOutstanding)*float(currentPrice)
        print(name)
        print(ticker)
        print(currentPrice)
        print(sharesOutstanding)
        print(marketCap)
        print("-----------")


def getCurrentPrice(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/price"
    price = requests.get(url)
    return json.loads(price.text)


def getOutStandingShare(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/stats"
    r = requests.get(url)
    stats = json.loads(r.text)
    return stats["sharesOutstanding"]

def readable(number):

def getFinancials(ticker):


getAllTickers()
#getCurrentPrice("A")
