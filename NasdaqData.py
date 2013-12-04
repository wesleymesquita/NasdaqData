import os
import datetime
import pandas.io.data as web

from pandas.core.frame import DataFrame


def getNasdaqTickerList( fileLocation ):
    """ Parses the CSV File containing basic info 
    about companies listed in NASDAQ. Go to 
    http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ 
    to get a fresh version """
    ticker_list = []
    try:
        csv_file = open(fileLocation, "r")
        lines = csv_file.readlines();
        
        if len(lines) == 0:
            print "[Error] getTickerList : no tickers! "
            return False 
        
        for line in lines:
            items = line.split(",")
            ticker_list.append(items[0].replace("\"", ""))             
        csv_file.close()
        return ticker_list
    except IOError as ioe:
        print "Error in getTickerList", ioe 
    except:
        print "Unknown exception in getTickerList"


def getClosingPrices(ticker, start, end, source="yahoo"):
    """ Get the closing prices for stock with symbol TICKER,
    from SOURCE ('yahoo' or 'google'), in the period among
    START and END """ 
    data = web.DataReader(ticker, source, start, end)
    closing_prices  = data['Close']
    return closing_prices

def getOpeningPrices(ticker, start, end, source="yahoo"):
    """ Get the closing prices for stock with symbol TICKER,
    from SOURCE ('yahoo' or 'google'), in the period among
    START and END """ 
    data = web.DataReader(ticker, source, start, end)
    opening_prices  = data['Open']
    return opening_prices

def createClosingPriceDataFrame(tickerList):
    d = {}
    for ticker in tickerList[1:10]:
        try:
            closing_prices = getClosingPrices(ticker, datetime.datetime(2013, 10, 1),  datetime.datetime(2013, 10, 10) )
            d[ticker] = closing_prices
        except:
            pass
    return DataFrame(d)

def dataFrameToCSV(dataframe, filename):
    """ Dumps a dataframe in 'filename'
    """
    DataFrame.to_csv(dataframe, filename)

####################

def test_getTicker():
    temp_CSV = open("temp_file.csv", "w");
    temp_CSV.write('"FCTY","1st Century Bancshares, Inc","6.79","63000356.37","n/a","n/a","Finance","Major Banks","http://www.nasdaq.com/symbol/fcty",')
    temp_CSV.write("\n")
    temp_CSV.write('"ADUS","Addus HomeCare Corporation","29","316476217","n/a","2009","Health Care","Medical/Nursing Services","http://www.nasdaq.com/symbol/adus",')
    temp_CSV.close()
    
    expected_ticker_list  = ["FCTY", "ADUS"]
    ticker_list = getNasdaqTickerList("temp_file.csv")
    
    os.remove("temp_file.csv")
    
    if ticker_list != expected_ticker_list:
        return False
    else:
        return True

def test_getClosingPrice():
    closing_prices_yahoo = getClosingPrices('MSFT', datetime.datetime(2012, 10, 1),  datetime.datetime(2013, 2, 1), 'yahoo')
    closing_prices_google = getClosingPrices('MSFT', datetime.datetime(2012, 10, 1),  datetime.datetime(2013, 2, 1), 'google')
    
    if len(closing_prices_google) != len(closing_prices_yahoo):
        return False
    
    for date in closing_prices_yahoo.keys():
        if abs(closing_prices_google[date] - closing_prices_yahoo[date]) > 0.02:
            print abs(closing_prices_google[date] - closing_prices_yahoo[date]), "Error: getClosingPrice: GOOGLE:", closing_prices_google[date], " YAHOO: ", closing_prices_yahoo[date] 
            return False
    
    return True

def test_getOpeningPrice():
    opening_prices_yahoo = getOpeningPrices('MSFT', datetime.datetime(2012, 10, 1),  datetime.datetime(2013, 2, 1),'yahoo')
    opening_prices_google = getOpeningPrices('MSFT', datetime.datetime(2012, 10, 1),  datetime.datetime(2013, 2, 1), 'google')
    
    if len(opening_prices_google) != len(opening_prices_yahoo):
        return False
    
    for date in opening_prices_yahoo.keys():
        if abs(opening_prices_google[date] - opening_prices_yahoo[date]) > 0.02:
            print abs(opening_prices_google[date] - opening_prices_yahoo[date]), "Error: getClosingPrice: GOOGLE:", opening_prices_google[date], " YAHOO: ", opening_prices_yahoo[date] 
            return False
    
    return True

def test_dataFrameToCSV():
    tickers = ['MSFT', 'AAPL', 'BIDU', 'GOOG', 'NFLX']
    dt = createClosingPriceDataFrame(tickers);
    dataFrameToCSV(dt, "C:\\Users\\wesley\\Documents\\GitHub\\dataanalysis\\dataframe.txt")

def testAll():     
    print test_getTicker()
    print test_getClosingPrice()
    print test_getOpeningPrice()

def getClosingPricesTable(): 
    tickers = getNasdaqTickerList("companylist.csv");
    dt = createClosingPriceDataFrame(tickers);
    dataFrameToCSV(dt, "C:\\Users\\wesley\\Documents\\GitHub\\dataanalysis\\dataframe.txt")

getClosingPricesTable()

