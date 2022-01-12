
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from config import config_global



def load_csv():
    csv_dataframe = pd.read_csv(
        'list.csv', names=['symbols'])
    config_global.tickers_list = csv_dataframe.symbols.tolist()


def filter22():
  
    #download today's data
   # data=yf.download(config_global.tickers_list,period='1d', interval='1m')
    #for getting yesterday's data
    #data2 = yf.download(config_global.tickers_list, start=config_global.USER_INPUT_start_date,
            #    end=config_global.USER_INPUT_end_date, group_by='ticker')
    #print(data2)
    for config_global.symbol in config_global.tickers_list:
        data=yf.download(config_global.symbol,period='1d', interval='1m')
        data2 = yf.download(config_global.symbol, start=config_global.USER_INPUT_start_date,
                end=config_global.USER_INPUT_end_date, group_by='ticker')
        print(data2)
        if data2.empty == False:
            # Create a list of closing prices for each symbol and get yesterday's closing price
            config_global.closing_price = data2['Close'].tolist()
            config_global.yesterday_close_price = config_global.closing_price[-1]
        print(config_global.yesterday_close_price)   
        if data.empty== False:    
         # Create a list of closing prices for each symbol
            config_global.closing_prices_list = data['Close'].tolist()
            
            order=sorted(config_global.closing_prices_list,reverse=True)
            config_global.N,config_global.M=order[0],order[-1]
            
            operation()    
            

def operation():
    
    time = len(config_global.closing_prices_list)
    current_price = config_global.closing_prices_list[time-1]
    print(current_price)
    if (config_global.yesterday_close_price > current_price):
        #check if the price is down than today's highest price
        down_recent,down_first = down_trend(current_price)
        if(down_recent > down_first):
            config_global.down_percent.append((down_recent/config_global.yesterday_close_price)*100)
            config_global.down_trend_sym.append(config_global.symbol)
            
    else:
        #check if the price is up than today's lowest price
        up_recent,up_first = up_trend(current_price)
        if(up_recent > up_first):
            config_global.up_percent.append((up_recent/config_global.yesterday_close_price)*100)
            config_global.up_trend_sym.append(config_global.symbol)
            
            

def down_trend(current_price):
    down_recent = config_global.yesterday_close_price - current_price
    down_first = config_global.yesterday_close_price - config_global.N 
    return(down_recent, down_first)

def up_trend(current_price):
    up_recent = current_price - config_global.yesterday_close_price
    up_first = config_global.M - config_global.yesterday_close_price
    return(up_recent, up_first)

def print_data():
    # Store information in a dataframe and export a CSV
     d={"uptrend stock":config_global.up_trend_sym,
            "up percent" : config_global.up_percent,
           "downtrend stock":config_global.down_trend_sym,
           "down percent" : config_global.down_percent}
     final = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
     #rearrange data in descending order
   
     final.sort_values('up percent',axis=0,ascending=False, inplace=True,)
     #final.sort_values("down percent",axis=1,ascending=False, inplace=True,)
     
     final.set_index("uptrend stock",inplace=True)
     final.reset_index(inplace=True) 
     final.to_csv('uptrend and downtrend stocks.csv',index=False)
     
     print(final)  
     print(config_global.USER_INPUT_start_date,config_global.USER_INPUT_end_date)          

def get_date():
    
    #get current date and day
    now = datetime.today()
    config_global.day=now.strftime("%A")
    print(config_global.day)
    USER_INPUT_end_date_today = now.strftime("%Y-%m-%d")
     # This is to ensure that a data is available for comparision.
    if(config_global.day=='Sunday'):
        config_global.USER_INPUT_end_date = str(datetime.strptime(
            USER_INPUT_end_date_today, '%Y-%m-%d').date() - timedelta(days=2))
    elif(config_global.day=='Saturday'):
        config_global.USER_INPUT_end_date = str(datetime.strptime(
            USER_INPUT_end_date_today, '%Y-%m-%d').date() - timedelta(days=1))
    else:
        config_global.USER_INPUT_end_date = str(datetime.strptime(
            USER_INPUT_end_date_today, '%Y-%m-%d').date() - timedelta(days=0))        
    # Using timedelta of 5 because the stock market might be colsed before the end data.
   
    config_global.USER_INPUT_start_date = str(datetime.strptime(
        config_global.USER_INPUT_end_date, '%Y-%m-%d').date() - timedelta(days=5))  

             