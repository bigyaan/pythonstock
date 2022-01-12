import pandas as pd



# Initilization
csv_dataframe = top_n_stocks = top_n_stocks_dup = top_n_stocks_with_conditions = all_stock_info = all_stock_info_dup = down_stock=pd.DataFrame()

# CSV name
csv_name = 'list.csv'
list_of_csv = []

# List of symbols
tickers_list = []

#open link in browser
open2=''

# List of closing prices for the current symbol
closing_prices_list = []
last_day_price_change = 0.0
percent_change = 0.0

# This stores the currently processing symbol
symbol = ''


# All variables from the compute engine
DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up = 0
DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down = 0

no_of_up_trend = 0
no_of_down_trend = 0

DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend = []
DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend = []

LIST_amount_change_per_uptrend = []
LIST_amount_change_per_downtrend = []

DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend = []
DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend = []

DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends = 0
DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends = 0

# Count of days in a up or down trend
days_count_for_up_trend = 0
days_count_for_down_trend = 0

DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends = []
DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends = []

DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends = 0
DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends = 0

DAY_DATA_IND_STOCK_last_closing_price = 0
DAY_DATA_IND_STOCK_average_price_input_Period = 0


# Percent chance
uptrend_flag = 0
no_of_uptrends_with_days_greater_than_threshold = 0
computed_percent_chance = 0.0
list_of_percent_chance = []
list_of_market_capital = []
list_of_52weeks_high = []
list_of_52weeks_low = []


# -------------------------------------------





# Analysis
LIST_IND_STOCK_NO_OF_DAYS_PRICE_DOWN = 0
LIST_IND_STOCK_NO_OF_DAYS_PRICE_UP = 0
LIST_IND_STOCK_AMOUNT_PRICE_UP = 0
LIST_IND_STOCK_AMOUNT_PRICE_DOWN = 0
ALL_IND_STOCK_NO_OF_DAYS_AVG_PRICE_UP = 0

#
USER_INPUT_DAY_UP_TREND = 0

#filter_day_n_minus_m filter
data2=pd.DataFrame()
tickers_list=[]
closing_prices_list=[]
down_stock_sym=[]
down_stock_val=[]
stock_price_at_M=[]
stock_price_at_N=[]
closing_price_now=[]
date_time_for=[]
time_N=[]
time_M=[]
symbol=''
USER_INPUT_percent_price_down=0.0
calculated_change=[]
down=[]
itr=''
date_for = []

#uptrend downtrend stocks
up_trend_sym=[]
down_trend_sym=[]
up_percent=[]
down_percent=[]
closing_prices_list=[]
symbol=''
N,M=0.0,0.0
yesterday_close_price=0.0
USER_INPUT_end_date,USER_INPUT_start_date='',''
day=''

#task3_highest_difference
high_list=[]
low_list=[]
el=[]
average_list=[]
symbol_list=[]
ranges=0


# delisted stocks
delisted_list=[]



trend=[]
LLLHH_chance=[]
trend_list=[]
iter_list=[]
USER_INPUT_LLLHH = ''