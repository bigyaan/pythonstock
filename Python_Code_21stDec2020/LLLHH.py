#import sys
import pandas as pd
from config import config_global
#from config import config_print_stock_details
#from config import config_userinput


def next_trend_analysis():
    #if config_global.all_stock_info.index.size:
       # config_global.iter_list = config_global.all_stock_info['symbol'].to_list()
       # config_global.all_stock_info.set_index('symbol', inplace=True)
        config_global.all_stock_info_dup = config_global.all_stock_info.copy(deep = True)
        config_global.all_stock_info_dup.set_index('symbol', inplace=True)    
        for config_global.symbol in config_global.tickers_list:
            config_global.trend_list = []
            count1= 0
            count2= 0
            config_global.trend_list = config_global.all_stock_info_dup['trend'][config_global.symbol]
            for itr in range(1,len(config_global.trend_list)):
                if(config_global.trend_list[itr-1] == -2):
                    if(config_global.trend_list[itr] == 2):
                        count1 += 1
                    elif(config_global.trend_list[itr] <= 2):
                        count2 +=1

            config_global.LLLHH_chance.append((count1 / count2) *100)                

def print_data():
    # Store information in a dataframe and export a CSV
     dict={" stock":config_global.tickers_list,
            "percent chance LLLHH" : config_global.LLLHH_chance}
     final = pd.DataFrame(dict)
     #rearrange data in descending order
   
     final.sort_values('percent chance LLLHH',axis=0,ascending=False, inplace=True,)
     
     final.set_index("percent chance LLLHH",inplace=True)
     final.reset_index(inplace=True) 
     final.to_csv('LLLHH.csv',index=False)
     print(final)  
           
            

