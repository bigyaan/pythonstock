import sys
import yfinance as yf
import pandas as pd

from config import config_global
from config import config_userinput

import compute_engine


def single_stock_analysis():
    """
    Function for analyzing a single stock
    """
    data = yf.download(config_userinput.USER_INPUT_SINGLE_STOCK_ANALYSIS_STOCK_SYMBOL, start=config_userinput.USER_INPUT_start_date,
                       end=config_userinput.USER_INPUT_end_date, group_by='ticker')

    config_global.closing_prices_list = data['Close'].to_list()

    # Same compute function can work for single and multiple stocks.
    # Another function is required if variables are different.
    config_global.symbol = config_userinput.USER_INPUT_SINGLE_STOCK_ANALYSIS_STOCK_SYMBOL
    compute_engine.compute(singleStock=True)


def percent_chance_filter1():

    print('\nCalculating percent chance...')

    # Changing the index of the dataframe to make data easily accessible
    #config_global.all_stock_info_dup = config_global.all_stock_info.copy(deep = True)
    config_global.all_stock_info.set_index('symbol', inplace=True)

    for config_global.symbol in config_global.tickers_list:
        # Compute percent chance only if there was at least one uptrend and the last uptrend was just starting
        if config_global.all_stock_info['no_of_up_trend'][config_global.symbol] and config_global.all_stock_info['uptrend_flag'][config_global.symbol]:

            # Clear variables before calculating for next symbol
            config_global.no_of_uptrends_with_days_greater_than_threshold = 0
            config_global.computed_percent_chance = 0

            # Get number of uptrends with days greater than USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD
            config_global.no_of_uptrends_with_days_greater_than_threshold = sum([1
                                                                                 # Retrieving data from dataframe
                                                                                 for x in config_global.all_stock_info['DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend'][config_global.symbol]
                                                                                 if x > config_userinput.USER_INPUT_AVERAGE_NO_OF_DAYS_UP_THRESHOLD])

            # Calculate percent chance
            config_global.computed_percent_chance = (
                config_global.no_of_uptrends_with_days_greater_than_threshold / config_global.all_stock_info['no_of_up_trend'][config_global.symbol]) * 100

            # If user wants a csv of stocks with higher percent chance
            if config_userinput.USER_INPUT_write_csv == 'y':
                # Keep stock information in lists if percent chance is higher
                if config_global.computed_percent_chance > config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE:
                    config_global.list_of_percent_chance.append(
                        config_global.computed_percent_chance)

                    # If user wants csv of stock with conditions
                    if config_userinput.USER_INPUT_write_csv_with_conditions == 'y':
                        # Get market capital, 52 weeks high and low
                        stock_info = yf.Ticker(config_global.symbol)
                        config_global.list_of_market_capital.append(
                            stock_info.info['marketCap']/1000000000)  # In billions
                        config_global.list_of_52weeks_high.append(
                            stock_info.info['fiftyTwoWeekHigh'])
                        config_global.list_of_52weeks_low.append(
                            stock_info.info['fiftyTwoWeekLow'])
                else:
                    # Drop the entire information of the stock from the dataframe
                    config_global.all_stock_info.drop(
                        index=config_global.symbol, inplace=True)
        else:
            # Drop the entire information of the stock from the dataframe
            config_global.all_stock_info.drop(
                index=config_global.symbol, inplace=True)

    # Keep recently computed information in the dataframe
    # Adding information in a dataframe in a loop is inefficient
    # So adding the information from a list
    if config_userinput.USER_INPUT_write_csv == 'y':
        config_global.all_stock_info['computed_percent_chance'] = config_global.list_of_percent_chance
        if config_userinput.USER_INPUT_write_csv_with_conditions == 'y':
            config_global.all_stock_info['MarketCapital'] = config_global.list_of_market_capital
            config_global.all_stock_info['fiftyTwoWeeksHigh'] = config_global.list_of_52weeks_high
            config_global.all_stock_info['fiftyTwoWeeksLow'] = config_global.list_of_52weeks_low

    # Reset the index of the dataframe
    config_global.all_stock_info.reset_index(drop=False, inplace=True)

    if not config_global.all_stock_info.index.size:
        print('\nThere are no stocks with percent chance greater than ',
              config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, '.')
        sys.exit(0)
