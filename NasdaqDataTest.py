import NasdaqDataRetriever as ndr

import datetime as dt
import os
import tempfile
import unittest

class TestNasdaqDataRetriever(unittest.TestCase):

    def test_getNasdaqTickerList(self):
        
        temp_CSV, fname = tempfile.mkstemp()
        temp_CSV.write('"FCTY","1st Century Bancshares, Inc","6.79","63000356.37","n/a","n/a","Finance","Major Banks","http://www.nasdaq.com/symbol/fcty",')
        temp_CSV.write("\n")
        temp_CSV.write('"ADUS","Addus HomeCare Corporation","29","316476217","n/a","2009","Health Care","Medical/Nursing Services","http://www.nasdaq.com/symbol/adus",')
        temp_CSV.close()
    
        expected_ticker_list = ["FCTY", "ADUS"]
        ticker_list = ndr.getNasdaqTickerList("temp_file.csv")
        
        os.unlink(fname)
        
        self.assertEqual(ticker_list, expected_ticker_list, "getTicker failed")
        
    def test_getClosingPrice(self):
        closing_prices_yahoo = ndr.getClosingPrices('MSFT', dt.datetime(2012, 10, 1), dt.datetime(2013, 2, 1), 'yahoo')
        closing_prices_google = ndr.getClosingPrices('MSFT', dt.datetime(2012, 10, 1), dt.datetime(2013, 2, 1), 'google')
    
        self.assertEqual(len(closing_prices_google), len(closing_prices_yahoo), "getClosingPrices get different number of items for the same company")
    
        for date in closing_prices_yahoo.keys():
            self.assertFalse(abs(closing_prices_google[date] - closing_prices_yahoo[date]) > 0.02, "Got a diffence greater then 0.02 in prices from different sources")
        
    def test_getOpeningPrice(self):
        opening_prices_yahoo = ndr.getOpeningPrices('MSFT', dt.datetime(2012, 10, 1), dt.datetime(2013, 2, 1), 'yahoo')
        opening_prices_google = ndr.getOpeningPrices('MSFT', dt.datetime(2012, 10, 1), dt.datetime(2013, 2, 1), 'google')
        
        self.assertEqual(len(opening_prices_google), len(opening_prices_yahoo), "getClosingPrices get different number of items for the same company")
    
        for date in opening_prices_yahoo.keys():
            self.assertFalse(abs(opening_prices_google[date] - opening_prices_yahoo[date]) > 0.02, "Got a diffence greater then 0.02 in prices from different sources")
        
    def test_dataFrameToCSV(self):
        tickers = ['MSFT', 'AAPL', 'BIDU', 'GOOG', 'NFLX']
        dt = ndr.createClosingPriceDataFrame(tickers);
        fd, name = tempfile.mkstemp()
        ndr.dataFrameToCSV(dt, name)
        fd.close()
        os.unlink(name)
        
    def getClosingPricesTable(self): 
        tickers = ndr.getNasdaqTickerList("companylist.csv");
        dt = ndr.createClosingPriceDataFrame(tickers);
        fd, name = tempfile.mkstemp()        
        ndr.dataFrameToCSV(dt, name)
        fd.close()
        os.unlink(name)
        
    def test_createClosingPriceDataFrame(self):   
        try:
           ndr.createClosingPriceDataFrame(['MSFT', 'GOOG'], dt.date(2013, 10, 10), dt.date(2012, 10, 10), -1, -1)
        except:
            
