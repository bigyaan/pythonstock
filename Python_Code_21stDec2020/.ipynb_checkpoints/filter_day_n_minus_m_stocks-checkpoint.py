import yfinance as yf
import pandas as pd
from datetime import datetime
from config import config_global


def start_code():
    
    # get the N-M vaule from the user in negative value
    config_global.USER_INPUT_percent_price_down=float(input('Enter the percent price down in negative value : '))




def filter11():
  
    for config_global.symbol in config_global.tickers_list:
        config_global.data2=pd.DataFrame()
        config_global.closing_prices_list = []
        date_time = []
        date_time_for = []
        config_global.date_for = []
           
         # Create a list of closing prices for each symbol
        data=yf.download(config_global.symbol,period='1d', interval='1m')
        if data.empty== False:
            config_global.closing_prices_list = data['Close'].tolist()
            date_time=list(data.index.tolist())
    
            #format the timestamp
            for config_global.itr in date_time:
              date_time_for.append(datetime.strftime(config_global.itr,"%m/%d/%Y, %H:%M:%S"))   
            #create dataframe for sorting date with respect to price
            dict={'Datetime':date_time_for,
                  'Close':config_global.closing_prices_list}

            config_global.data2=pd.DataFrame(dict)
            config_global.data2.sort_values(by='Close',ascending=False,inplace=True)
            operation()

def operation():
    
    # Clear all variables before analyzing every stock symbol
    percent_price_down=0.0
    average=0.0
    N,M=0.0,0.0
    
    #sort dataframe with respect to closing price
    config_global.data2.sort_values(by='Close',ascending=False,inplace=True)
    config_global.date_for = config_global.data2['Datetime'].tolist()
    
    #sorting closing price in descending order
    order=sorted(config_global.closing_prices_list,reverse=True)
    config_global.down=[]         
    N,M=order[0],order[-1]
    
    #calculate percent change between M and N  
    change=((M-N)/M)*100
    config_global.calculated_change.append(change)

    # Process percent price down for current symmbol starting from last date
    
    for index in range(len(config_global.closing_prices_list),0,-1):
        #previous_price = closing_prices_list[index-2]
        current_price = config_global.closing_prices_list[index-1]
        percent_price_down=((current_price-N)/N)*100

        if (percent_price_down < config_global.USER_INPUT_percent_price_down):
            config_global.down.append(percent_price_down)
    try:    
        average=sum(config_global.down)/len(config_global.down)       
    except ZeroDivisionError:
        print('----------')
    # Store all computed information in a dataframe        
    if (average < config_global.USER_INPUT_percent_price_down):        
        config_global.down_stock_sym.append(config_global.symbol)
        config_global.down_stock_val.append(average)    
        config_global.stock_price_at_N.append(N)
        config_global.time_N.append(config_global.date_for[0])
        config_global.stock_price_at_M.append(M)
        config_global.time_M.append(config_global.date_for[-1])
        config_global.closing_price_now.append(config_global.closing_prices_list[-1])

def print_data():
     # Store information in a dataframe and export a CSV
     dict={"stock":config_global.down_stock_sym,
           "price down":config_global.down_stock_val,
           "stock price at N":config_global.stock_price_at_N,
           "time N":config_global.time_N,
           "stock price at M":config_global.stock_price_at_M,
           "time M":config_global.time_M,
           "closing price now":config_global.closing_price_now}
     final = pd.DataFrame(dict)
     #rearrange data in ascending order
     final.sort_values("price down",axis=0,ascending=True, inplace=True,)
     final.set_index("stock",inplace=True)
     final.reset_index(inplace=True)
     final.to_csv('N-M_down_stocks.csv',index=False)
     

     print(final)
     try:
         calculated_change_average=sum(config_global.calculated_change)/len(config_global.calculated_change)
         print(f"the average percent diffenrence between N and M as seen in the meket is {calculated_change_average}")
    
     except ZeroDivisionError:
        print("zero division")