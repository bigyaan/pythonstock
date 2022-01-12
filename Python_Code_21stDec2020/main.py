from os import path

from config import config_global
from config import config_userinput

import request_input
import csv_processor
import compute_engine
import daydata_analysis_filters
import print_stock_details
import open_browser
import util
import counter_top_n_stocks
import filter_day_n_minus_m_stocks
import low_high_momentum
import uptrend_downtrend_in_a_day
import spiketime
import task_3_highest_difference
import delisted
import LLLHH

request_input.show_filters()

if config_userinput.USER_INPUT_MULTIPLE_STOCK_ANALYSIS == 1:
    # Ask for user input or load from input file
    if not path.exists('input.csv'):
        request_input.daybased_inputs()
    else:
        request_input.load_from_file()

    csv_processor.load_csv()
    compute_engine.compute()

    config_global.USER_INPUT_LLLHH = input('Do you want to calculate percent chance based on L L L H H sequence?? :').lower()
    if config_global.USER_INPUT_LLLHH == 'y':
        LLLHH.next_trend_analysis()
        LLLHH.print_data()



    if config_userinput.USER_INPUT_compute_percent_chance == 'y':
        daydata_analysis_filters.percent_chance_filter1()
        if config_userinput.USER_INPUT_write_csv == 'y':
            csv_processor.write_csv()
            print_stock_details.print_stocks_with_high_pc()
            if config_userinput.USER_INPUT_print_info_for_top_n_stocks == 'y':
                print_stock_details.Day_Data_Print_Verbose()
            else:
                print_stock_details.print_summary()
            if config_userinput.USER_INPUT_open_browser == 'y':
                count_data = counter_top_n_stocks.counter2()
                print(f"The number of data in top N stocks is {count_data}")
                config_global.open2 = input('Do you want to open them in browser').lower()
                if config_global.open2 == 'y':
                    open_browser.open_in_tabs(
                        config_global.top_n_stocks.index.to_list())


elif config_userinput.USER_INPUT_SINGLE_STOCK_ANALYSIS == 1:
    request_input.singleStock()

    daydata_analysis_filters.single_stock_analysis()
    print_stock_details.Day_Data_Print_Verbose()
elif config_userinput.USER_INPUT_open_stock_link == 1:
    util.search_csv()
    request_input.get_csv_name()
    csv_processor.load_csv()
    open_browser.open_in_tabs(config_global.tickers_list)
elif config_userinput.USER_INPUT_analyze_top_n_csv == 1:
    util.search_csv()
    request_input.get_csv_name()
    request_input.get_dates()
    csv_processor.load_csv()
    compute_engine.compute()
    print_stock_details.print_summary()


elif config_userinput.USER_INPUT_momentum_stock_analysis == 1:
    # Ask for user input or load from input file
    low_high_momentum.get_info()
 

    csv_processor.load_csv()
    compute_engine.compute()

    if config_userinput.USER_INPUT_compute_percent_chance == 'y':
        daydata_analysis_filters.percent_chance_filter1()
        if config_userinput.USER_INPUT_write_csv == 'y':
            csv_processor.write_csv()
            print_stock_details.print_stocks_with_high_pc()
            if config_userinput.USER_INPUT_print_info_for_top_n_stocks == 'y':
                print_stock_details.Day_Data_Print_Verbose()
            else:
                print_stock_details.print_summary()
            if config_userinput.USER_INPUT_open_browser == 'y':
                open_browser.open_in_tabs(
                    config_global.top_n_stocks.index.to_list())  
                

    low_high_momentum.load_csv()
    low_high_momentum.per_high_cal()
    low_high_momentum.print_data()                  
   
       
elif config_userinput.USER_INPUT_analyze_nm == 1:
    filter_day_n_minus_m_stocks.start_code()
    csv_processor.load_csv()
    filter_day_n_minus_m_stocks.filter11()
    filter_day_n_minus_m_stocks.print_data()

elif config_userinput.USER_INPUT_uptrend_downtrend_stocks == 1:
    uptrend_downtrend_in_a_day.load_csv()
    uptrend_downtrend_in_a_day.get_date()
    uptrend_downtrend_in_a_day.filter22()
    uptrend_downtrend_in_a_day.print_data()
    
elif config_userinput.USER_INPUT_highest_difference_stock == 1:
    task_3_highest_difference.main_mod()  
elif config_userinput.USER_INPUT_delisted == 1:
    delisted.main_mod() 

elif config_userinput.USER_INPUT_timeslot == 1:
    # Ask for user input or load from input file
    if not path.exists('input.csv'):
        request_input.daybased_inputs()
    else:
        request_input.load_from_file()

    csv_processor.load_csv()
    compute_engine.compute()

    if config_userinput.USER_INPUT_compute_percent_chance == 'y':
        daydata_analysis_filters.percent_chance_filter1()
        if config_userinput.USER_INPUT_write_csv == 'y':
            csv_processor.write_csv()
            print_stock_details.print_stocks_with_high_pc()
            if config_userinput.USER_INPUT_print_info_for_top_n_stocks == 'y':
                print_stock_details.Day_Data_Print_Verbose()
            else:
                print_stock_details.print_summary()
            if config_userinput.USER_INPUT_open_browser == 'y':
                
                ### Task 10 : Count the number of data in top N stocks and ask if to open them in brower or not for last time
                count_data = counter_top_n_stocks.counter2()
                print(f"The number of data in top N stocks is {count_data}")
                config_global.open2 = input('Do you want to open them in browser').lower()
                if config_global.open2 == 'y':
                    open_browser.open_in_tabs(
                        config_global.top_n_stocks.index.to_list())
    spiketime.TimeSlot()           
else:
    pass
