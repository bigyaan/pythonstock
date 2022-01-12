import pandas as pd
from datetime import datetime, timedelta

from config import config_userinput
from config import config_global

import csv_processor


def show_filters():
    print('\n-----------------------------------------------------',
          '\nNOTE: FOR ALL QUESTIONS ENTER y FOR YES AND n FOR NO.',
          '\n-----------------------------------------------------')
    print('-----------------------------------------------------',
          '\nFollowing are the available filters.',
          '\nSelect the corresponding number to use it.',
          '\n-----------------------------------------------------')
    print('\n1. Day based multiple stock analysis',
          '\n2. Day based single stock analysis',
          '\n3. 15 minutes',
          '\n4. Open Yahoo Finance links for stocks in a CSV',
          '\n5. Analyze generated Top N CSV file',
          '\n6. Task 8: Get stocks that have momentum to carry tomorrow based on past six month',
          '\n7. Task 7: Get the stocks that have decreased by more than n-m% in present time',
          '\n8. Task 9: Get the uptrend and downtrend stocks list'
          '\n9. Task 3: Get stocks that have shown highest difference between days range'
          '\n10. Task 5: Get delisted stocks'
          '\n11. Task 1: Get time slots where a stock usually spike based on top N stocks'
          '\n\n-----------------------------------------------------')
    config_userinput.USER_INPUT_filter_selection = int(
        input('Select a number : '))

    # Assign the selection input to corresponding variable
    if config_userinput.USER_INPUT_filter_selection == 1:
        config_userinput.USER_INPUT_MULTIPLE_STOCK_ANALYSIS = 1
    elif config_userinput.USER_INPUT_filter_selection == 2:
        config_userinput.USER_INPUT_SINGLE_STOCK_ANALYSIS = 1
    elif config_userinput.USER_INPUT_filter_selection == 4:
        config_userinput.USER_INPUT_open_stock_link = 1
    elif config_userinput.USER_INPUT_filter_selection == 5:
        config_userinput.USER_INPUT_analyze_top_n_csv = 1
    elif config_userinput.USER_INPUT_filter_selection == 6:
        config_userinput.USER_INPUT_momentum_stock_analysis = 1

    elif config_userinput.USER_INPUT_filter_selection == 7:
         config_userinput.USER_INPUT_analyze_nm =1   
    elif config_userinput.USER_INPUT_filter_selection == 8:
        config_userinput.USER_INPUT_uptrend_downtrend_stocks = 1 
    elif config_userinput.USER_INPUT_filter_selection == 9:
        config_userinput.USER_INPUT_highest_difference_stock = 1
    elif config_userinput.USER_INPUT_filter_selection == 10:
        config_userinput.USER_INPUT_delisted = 1  
    elif config_userinput.USER_INPUT_filter_selection == 11:
        config_userinput.USER_INPUT_timeslot = 1       
    else:
        pass


def daybased_inputs():
    config_userinput.USER_INPUT_start_date = input(
        'Enter the start date (yyyy-mm-dd): ')
    config_userinput.USER_INPUT_end_date = input(
        'Enter the end date (yyyy-mm-dd): ')
    config_userinput.USER_INPUT_compute_percent_chance = input(
        'Compute percent chance? ').lower()

    if config_userinput.USER_INPUT_compute_percent_chance == 'y':
        config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE = float(
            input('Enter percent chance value : '))
        config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD = int(
            input('Enter no. of days threshold : '))
        config_userinput.USER_INPUT_write_csv = input(
            'Do you want CSVs of stocks with higher percent chance? ').lower()

        if config_userinput.USER_INPUT_write_csv == 'y':
            config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS = int(
                input('How many stocks to filter as top N? '))
            if config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS:
                config_userinput.USER_INPUT_open_browser = input(
                    'Open links to Top N stocks in a browser? ')
                config_userinput.USER_INPUT_print_info_for_top_n_stocks = input(
                    'Print verbose information for the Top N stocks? ')
                config_userinput.USER_INPUT_write_csv_with_conditions = input(
                    'Do you want to filter stocks based on Market Capital and 52 Weeks High/Low? ').lower()

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


def singleStock():
    """
    Asks for user inputs for single stock analysis
    """
    config_userinput.USER_INPUT_SINGLE_STOCK_ANALYSIS_STOCK_SYMBOL = input(
        'Enter stock symbol : ').upper()
    # Single stock analysis requires all inputs required for daybased analysis
    daybased_inputs()


def load_from_file():
    config_userinput.load_input_file = input(
        'Input file found. Load inputs from it? ').lower()
    if config_userinput.load_input_file == 'y':
        config_userinput.user_input = pd.read_csv(
            'input.csv', header=0, index_col=0)
        # Ask for user input if any data is missing
        if config_userinput.user_input.isnull().any().any():
            print('\nRequired parameters absent in the input file!!!\n')
            daybased_inputs()
        else:
            # Read from input file to variables
            config_userinput.USER_INPUT_start_date, \
                config_userinput.USER_INPUT_end_date, \
                config_userinput.USER_INPUT_compute_percent_chance, \
                config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, \
                config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD, \
                config_userinput.USER_INPUT_write_csv, \
                config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS, \
                config_userinput.USER_INPUT_open_browser, \
                config_userinput.USER_INPUT_print_info_for_top_n_stocks, \
                config_userinput.USER_INPUT_write_csv_with_conditions, \
                config_userinput.USER_INPUT_market_capital, \
                config_userinput.USER_INPUT_fiftyTwoWeeksHigh, \
                config_userinput.USER_INPUT_fiftyTwoWeeksLow = pd.to_numeric(
                    config_userinput.user_input['value'], errors='coerce').combine_first(config_userinput.user_input['value']).values.tolist()
    else:
        daybased_inputs()


def get_csv_name():

    print('\nCSVs in the working directory...',)
    for i in range(0, len(config_global.list_of_csv)):
        print(i + 1, '. ', config_global.list_of_csv[i], sep='')

    print('-' * 53)

    if config_userinput.USER_INPUT_analyze_top_n_csv == 1:
        print('Which CSV to use to get Top N stocks?')
    # Get name of the CSV based on user input
    config_global.csv_name = config_global.list_of_csv[int(
        input('Select a number: ')) - 1]


def get_dates():
    config_userinput.USER_INPUT_end_date = input(
        'Enter the end date (yyyy-mm-dd): ')
    # Using timedelta of 5 because the stock market might be colsed before the end data.
    # Having a value greater than 1 won't affect the output.
    # This is just to ensure that a data is available for comparision.
    config_userinput.USER_INPUT_start_date = str(datetime.strptime(
        config_userinput.USER_INPUT_end_date, '%Y-%m-%d').date() - timedelta(days=5))
