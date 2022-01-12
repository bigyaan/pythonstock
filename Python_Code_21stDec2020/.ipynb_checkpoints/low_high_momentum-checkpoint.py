
import yfinance as yf
import pandas as pd
from config import config_userinput
from datetime import datetime, timedelta

tickers_list=[]
closing_prices_list=[] 
stock_info=[]
stock_price = []
#sym=[]

#def get_target_price():
    #global USER_INPUT_target_price
    #USER_INPUT_target_price=float(input("Enter the price target in percent : "))
    
def load_csv():
    global tickers_list
    csv_dataframe = pd.read_csv(
        'top_n_stocks.csv', names=['symbols'])
    tickers_list = csv_dataframe.symbols.tolist()
    
def per_high_cal():
    #high_percent=0
    print('\nRetrieving data for top n stocks...')
    print('\ncalculating present data and momentum chance......')
    data=yf.download(tickers_list,period='2d')
    
    for symbol in tickers_list:
        
        # Create a list of closing prices for each symbol
        if data.empty== False:
           closing_prices_list = data['Close'][symbol].tolist()
           for index in range(1, len(closing_prices_list)):
               previous_price = closing_prices_list[index-1]
               current_price = closing_prices_list[index]
               if(current_price>previous_price):
                   high=((current_price-previous_price)/current_price)*100
                   print(high)
                   #sym.append(high)
                   #for ind in range(high):
                   #for i in range(high_percent):
                   if (high>2):
                        stock_info.append(symbol)
                        stock_price.append(high)
def print_data():
    # Store information in a dataframe and export a CSV
    dict={"symbol":stock_info,
           "high":stock_price}
    final = pd.DataFrame(dict)
    #rearrange data in ascending order
    final.sort_values("high",axis=0,ascending=True, inplace=True,)
    final.set_index("symbol",inplace=True)
    final.reset_index(inplace=True)
    final.to_csv('%high.csv',index=False)
    print('\n the stocks to carry momentum : ') 
    print(final)

def get_info():
    now = datetime.today()
    config_userinput.USER_INPUT_end_date_today = now.strftime("%Y-%m-%d")
    config_userinput.USER_INPUT_end_date = str(datetime.strptime(
        config_userinput.USER_INPUT_end_date_today, '%Y-%m-%d').date() - timedelta(days=0))

    config_userinput.USER_INPUT_start_date = str(datetime.strptime(
        config_userinput.USER_INPUT_end_date, '%Y-%m-%d').date() - timedelta(days=180))  

    config_userinput.USER_INPUT_compute_percent_chance = 'y'
    config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD = 1
    config_userinput.USER_INPUT_write_csv = 'y'
    config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS = 30

    if config_userinput.USER_INPUT_compute_percent_chance == 'y':
        config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE = float(
            input('Enter percent chance value : '))

        if config_userinput.USER_INPUT_write_csv == 'y':
           # config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS = int(
               # input('How many stocks to filter as top N? '))
            if config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS:
                config_userinput.USER_INPUT_open_browser = 'n'
                config_userinput.USER_INPUT_print_info_for_top_n_stocks = input(
                    'Print verbose information for the Top N stocks? ')
                config_userinput.USER_INPUT_write_csv_with_conditions = 'n'

                if config_userinput.USER_INPUT_write_csv_with_conditions == 'y':
                    config_userinput.USER_INPUT_market_capital = int(
                        input('Enter market capital (in billions) : '))
                    config_userinput.USER_INPUT_fiftyTwoWeeksHigh = int(
                        input('Enter 52 weeks high : '))
                    config_userinput.USER_INPUT_fiftyTwoWeeksLow = int(
                        input('Enter 52 weeks low : '))

    # Store information in a dataframe and export a CSV
    config_userinput.user_input = pd.DataFrame([
        config_userinput.USER_INPUT_start_date,
        config_userinput.USER_INPUT_end_date,
        config_userinput.USER_INPUT_compute_percent_chance,
        config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE,
        config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD,
        config_userinput.USER_INPUT_write_csv,
        config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS,
        config_userinput.USER_INPUT_open_browser,
        config_userinput.USER_INPUT_print_info_for_top_n_stocks,
        config_userinput.USER_INPUT_write_csv_with_conditions,
        config_userinput.USER_INPUT_market_capital,
        config_userinput.USER_INPUT_fiftyTwoWeeksHigh,
        config_userinput.USER_INPUT_fiftyTwoWeeksLow
    ], columns=['value'], index=[
        'config_userinput.USER_INPUT_start_date',
        'config_userinput.USER_INPUT_end_date',
        'config_userinput.USER_INPUT_compute_percent_chance',
        'config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE',
        'config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD',
        'config_userinput.USER_INPUT_write_csv',
        'config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS',
        'config_userinput.USER_INPUT_open_browser',
        'config_userinput.USER_INPUT_print_info_for_top_n_stocks',
        'config_userinput.USER_INPUT_write_csv_with_conditions',
        'config_userinput.USER_INPUT_market_capital',
        'config_userinput.USER_INPUT_fiftyTwoWeeksHigh',
        'config_userinput.USER_INPUT_fiftyTwoWeeksLow'
    ])
    config_userinput.user_input.to_csv('input.csv')
    print(config_userinput.user_input)

                                 