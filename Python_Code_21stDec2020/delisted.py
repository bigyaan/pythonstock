import pandas as pd
import numpy as np
from config import config_global
import yfinance as yf
import csv

def main_mod():
    th = pd.read_csv ('list.csv' , names=['symbols'] )
    it = th ["symbols"].tolist()
    #print(it)
    
    for sym in it:
        x_df = yf.download(tickers=sym,start='2020-12-12',end='2021-01-01',progress=False)
        check=x_df.empty
        #print(check)
        
         
        if(check==False):
            config_global.delisted_list.append(sym)
            
    print(config_global.delisted_list)
    file = open('list2.csv', 'w+', newline ='') 
      
    # writing the data into the file 
    with file:     
        write = csv.writer(file) 
        write.writerows(config_global.delisted_list) 

