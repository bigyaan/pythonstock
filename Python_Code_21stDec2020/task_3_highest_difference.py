import pandas as pd
import yfinance as yf
from config import config_global
import numpy as np
##import matplotlib.pyplot as plts
def main_mod():
    th = pd.read_csv('list.csv' , names=['symbols'])
    it=th["symbols"].tolist()
   
    for sym in it:
        x_df = yf.download(tickers=sym,start='2020-12-12',end='2021-01-01',progress=False)
        #print(x_df)
        check=x_df.empty
        #print(check)
    
        if(check==False):
            config_global.high_list=x_df["High"].tolist()
            config_global.low_list=x_df["Low"].tolist()
            
            zip_file=zip(config_global.high_list,config_global.low_list)
            for list1,list2 in zip_file:
                config_global.ranges=abs(((list1-list2)/list2)*100)
                #print(ranges)
                config_global.el.append(config_global.ranges)
                
                #print(el)
            config_global.symbol_list.append(sym)
            #print(el)    
            average=sum(config_global.el)/len(config_global.el)
            config_global.average_list.append(average)
    #print(symbol_list)
        #print("The average for {} is {}".format(sym,average))
    df = pd.DataFrame(columns =['symbol','avg_per'])
    df["symbol"]=config_global.symbol_list
    df["avg_per"]=config_global.average_list
    df[df["avg_per"]>3]                                               
    print(df)