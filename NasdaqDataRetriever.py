import os
import datetime as dt
import pandas.io.data as web

from pandas.core.frame import DataFrame


"""
    @summary: NASDAQ Data Retriever is minimalist platform to get NASDAQ basic stock
              data prices 
    @requires: NumPy (http://www.numpy.org/), Pandas (http://pandas.pydata.org/)
    @author: Wesley Mesquita
    @contact:  wesleymesquita@gmail.com
"""

class NASDAQDataRetriverException(Exception):
    pass


def getNasdaqTickerList( ):
    """
    @summary: Parses the CSV File containing basic info 
            about companies listed in NASDAQ. There is a copy got 
            in December 4, 2013 in the repository. But go to 
            http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ 
            to get a fresh version. Save it as 'companylist.csv' in the same directory
            as this file     
    @return: a list of all NASDAQ Ticker Symbols
    """
    
    ticker_list = []
    try:
        csv_file = open("companylist.csv", "r")
        lines = csv_file.readlines();
        
        if len(lines) == 0:
            raise NASDAQDataRetriverException("No tickers available")
        
        for line in lines:
            items = line.split(",")
            ticker_list.append(items[0].replace("\"", ""))             
        csv_file.close()
        return ticker_list
    except IOError as ioe:
        raise NASDAQDataRetriverException("Error in getTickerList", ioe) 
    except:
        raise NASDAQDataRetriverException("Unknown exception in getTickerList")


def getPrices(ticker, category, start, end, source="yahoo"):
    """ 
    @summary: Get the closing prices for stock with symbol TICKER,
            from SOURCE ['yahoo', 'google'], in the period among
            START and END 
    @param ticker: Symbol Ticker of NASDAQ Company
    @param category: must be in ['Open', 'High', 'Low', 'Close'] 
    @param start: datetime object representing the start date  
    @param end: datetime object representing the end date
    @param source: supported ["yahoo", "google"]
    """ 
    if len(ticker) == 0:
        raise NASDAQDataRetriverException("No ticker!")
    if category not in ['Open', 'High', 'Low', 'Close']:
        raise NASDAQDataRetriverException("Invalid price category" + category)
    if end < start:
        raise NASDAQDataRetriverException("End date earlier than start date")    
    if source not in ['google', 'yahoo']:
        raise NASDAQDataRetriverException("Unsuported data source: " + source)     
       
    data = web.DataReader(ticker, source, start, end)
    prices  = data[category]
    return prices

def getOpeningPrices(ticker, start, end, source="yahoo"):
    """ Get the closing prices for stock with symbol TICKER,
    from SOURCE ('yahoo' or 'google'), in the period among
    START and END """ 
    return getPrices(ticker, 'Open', start, end, source)

def createPriceDataFrame(tickerList, category, source, date_start, date_end, from_index, to_index):
    """ 
    @summary: Get a pandas.DataFrame with each colunm representing a company
    and each line is a date.
    @param  tickerList: list containg NASDAQ ticker symbols 
    @param category: must be in ['Open', 'High', 'Low', 'Close']     
    @param source: supported ["yahoo", "google"]   
    @param date_start: datetime.date object representing the first date 
                       to aquire data
    @param date_end: datetime.date object representing the last date 
                     to aquire data  
    @param from_index and to_index: integer indexes to get an interval
                                    over ticker. If one of them is negative
                                    the entire tickerList will be considered
    """
    
    if date_end < date_start:
        raise NASDAQDataRetriverException("date_start must be greater than date_end")
    if to_index < from_index:
        raise NASDAQDataRetriverException("to_index lower than from_index")
            
    d = {}
    for ticker in tickerList[from_index:to_index]:
        closing_prices = getPrices(ticker, category, date_start,  date_end )
        d[ticker] = closing_prices
    return DataFrame(d)

def dataFrameToCSV(dataframe, filename):
    """ 
    @summary: Dumps a dataframe in 'filename'
    """
    DataFrame.to_csv(dataframe, filename)

def showTickerSymbolsIndexed(n_columns):
    ticker_list = getNasdaqTickerList()
     
    print_list = [{i:ticker_list[i]} for i in range(0, len(ticker_list))]
           
    for i in range(0, len(print_list), n_columns):
        print print_list[i:i+n_columns], "\n"
####################

showTickerSymbolsIndexed(10)
