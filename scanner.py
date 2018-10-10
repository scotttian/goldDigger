import requests
import json
import csv
from datetime import datetime

def parseable(text):
    try:
        return json.loads(text)
    except ValueError as e:
        return None # or: raise

def getAllTickers():
    url = "https://api.iextrading.com/1.0/ref-data/symbols"
    r = requests.get(url)
    all_stock_json_data = json.loads(r.text)
    all = []
    count = 0
    for stock in all_stock_json_data:
        count +=1
        newObject={}
        name = stock["name"]
        ticker = stock["symbol"]
        print(name)
        print(ticker)
        if not stock["isEnabled"]:
            continue
        currentPrice = getCurrentPrice(ticker)
        sharesOutstanding = getOutStandingShare(ticker) if getOutStandingShare(ticker) else 0
        marketCap = float(sharesOutstanding)*float(currentPrice)
        financial_JSON = getFinancials(ticker,False)
        annaul_financial_JSON = getFinancials(ticker,True)
        totalRevenue = 0
        netIncome = 0
        if "financials" in financial_JSON:
            for month in financial_JSON['financials']:
                if month['totalRevenue']:
                    totalRevenue = totalRevenue + float(month['totalRevenue'])
                if month['netIncome']:
                    netIncome = netIncome + float(month['netIncome'])
        if "financials" in annaul_financial_JSON:
            if len(annaul_financial_JSON['financials'])>=2:
                if "totalRevenue" in annaul_financial_JSON['financials'][0] and "totalRevenue" in annaul_financial_JSON['financials'][1] and annaul_financial_JSON['financials'][0]['totalRevenue'] and annaul_financial_JSON['financials'][1]['totalRevenue']:
                    growth_revenue =  float(annaul_financial_JSON['financials'][0]["totalRevenue"]- annaul_financial_JSON['financials'][1]["totalRevenue"])/ abs(float(annaul_financial_JSON['financials'][1]["totalRevenue"]))
                else:
                    growth_revenue = 0;
                if "netIncome" in annaul_financial_JSON['financials'][0] and "netIncome" in annaul_financial_JSON['financials'][1] and annaul_financial_JSON['financials'][0]['netIncome'] and annaul_financial_JSON['financials'][1]['netIncome']:
                    growth_income =  float(annaul_financial_JSON['financials'][0]["netIncome"]- annaul_financial_JSON['financials'][1]["netIncome"])/ abs(float(annaul_financial_JSON['financials'][1]["netIncome"]))
                else:
                    growth_income = 0;
            else:
                growth_income = 0;
                growth_revenue = 0;
        else:
            growth_income = 0;
            growth_revenue = 0;
        sectorAndTags_json = getSectorAndTags(ticker)
        sector = sectorAndTags_json['sector']
        newObject['index']=count
        newObject['name']=name
        newObject['ticker']=ticker
        print(currentPrice)
        newObject['currentPrice']=currentPrice
        print(sharesOutstanding)
        newObject['sharesOutstanding']=sharesOutstanding
        print(marketCap)
        newObject['marketCap']=marketCap
        print(totalRevenue)
        newObject['totalRevenue']=totalRevenue
        print(netIncome)
        newObject['netIncome']=netIncome
        if totalRevenue!=0:
            print(marketCap/totalRevenue)
            newObject['marketCap_totalRevenue']=marketCap/totalRevenue
        else:
            newObject['marketCap_totalRevenue']=0
        if netIncome!=0:
            if sharesOutstanding!=0:
                print(netIncome/sharesOutstanding)
                newObject['netIncome_sharesOutstanding']=netIncome/sharesOutstanding
            else:
                newObject['netIncome_sharesOutstanding']=0
            print(marketCap/netIncome)
            newObject['marketCap_netIncome']=marketCap/netIncome
        else:
            newObject['netIncome_sharesOutstanding']=0
            newObject['marketCap_netIncome']=0
        print(sector)
        print(growth_revenue)
        print(growth_income)
        newObject['sector']=sector
        newObject['growth_revenue']=growth_revenue
        newObject['growth_income']=growth_income
        print("-----------")
        all.append(newObject)
        if count >2:
            break
    #print(all)
    sorted_list = sorted(all,  key=lambda a : a['marketCap_totalRevenue'])
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    with open("/opt/suntorytime/goldDigger/out/output"+now+".csv", 'wb') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow( [k for (k, v) in sorted_list[0].iteritems()])
        for cdr in sorted_list:
            wr.writerow( [v for (k, v) in cdr.iteritems()])


def getCurrentPrice(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/price"
    price = requests.get(url)
    if parseable(price.text):
        return json.loads(price.text)
    else:
        return "0"

def getStats(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/stats"
    r = requests.get(url)
    if parseable(r.text):
        stats = json.loads(r.text)
        return stats
    else:
        return None

def getOutStandingShare(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/stats"
    r = requests.get(url)
    if parseable(r.text):
        stats = json.loads(r.text)
        if "sharesOutstanding" in stats:
            return stats["sharesOutstanding"]
        else:
            return None
    else:
        return None

def getSectorAndTags(ticker):
    url = "https://api.iextrading.com/1.0/stock/"+ticker+"/company"
    company = requests.get(url)
    if parseable(company.text):
        return json.loads(company.text)
    else:
        return {"sector":""}

def getFinancials(ticker,annual):
    if(annual):
        url = "https://api.iextrading.com/1.0/stock/"+ticker+"/financials?period=annual"
    else:
        url = "https://api.iextrading.com/1.0/stock/"+ticker+"/financials"
    price = requests.get(url)
    if parseable(price.text):
        return json.loads(price.text)
    else:
        return {}


getAllTickers()
#print(getCurrentPrice("ARNC-"))
#getOutStandingShare("CWEN")
