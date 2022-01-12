# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:36:48 2021

@author: prajapati
"""

import pandas as pd
import yfinance as yf

symbol = ['TSLA','AMZN']
sy = yf.download(symbol,period="1mo",interval="15m")
#ss = sy.history(period="1mo",interval="30m")
#inf=yf.Ticker('TSLA')
#aa=inf.info['marketCap']
#bb=inf.info['fiftyTwoWeekHigh']
#cc=inf.info['fiftyTwoWeekLow']
#print(f'\n{aa}  \n{bb}  \n {cc}')
a=pd.DataFrame(sy)
for sym in symbol:
    aa=a[sym]['Close'].values.tolist()
    print(aa)
#bb=a['Close']
#sys=a.columns()
#print(bb)
#print(a.iloc[3])

#ii=yf.info(symbol)
#print(ii)

import yfinance as yf
import pandas as pd


tickers_list=[]
closing_prices_list=[]
down_stock_sym=[]
down_stock_val=[]
symbol=''
USER_INPUT_percent_price_down=0.0

def start_code():
    global USER_INPUT_percent_price_down
    USER_INPUT_percent_price_down=input('enter the percent price down ')

def load_csv():
    global tickers_list
    csv_dataframe = pd.read_csv(
        'list.csv', names=['symbols'])
    tickers_list = csv_dataframe.symbols.tolist()
    


def filter11():
    global closing_prices_list
    global symbol
    data=yf.download(tickers_list,period='1d', interval='1m')
    for symbol in tickers_list:
        #data=yf.download(symbol,period='1d', interval='1m')
        # Create a list of closing prices for each symbol
        aa=data.loc[("symbol","Close")]
        closing_prices_list = aa.tolist()
        order=sorted(closing_prices_list,reverse=True)
        print(order)
        print(closing_prices_list)
        operation()

def operation():
    
    # Clear all variables before analyzing every stock symbol
    percent_price_down=0.0

    # Process percent price down for current symmbol starting from last date
    
    for index in range(len(closing_prices_list),0,-1):
        previous_price = closing_prices_list[index-2]
        current_price = closing_prices_list[index-1]
 