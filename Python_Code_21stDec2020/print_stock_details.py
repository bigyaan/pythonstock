import sys

from config import config_global
from config import config_print_stock_details
from config import config_userinput


def Day_Data_Print_Verbose():
    if config_global.top_n_stocks.index.size:
        config_global.top_n_stocks_dup = config_global.top_n_stocks.copy(deep = True)  
        iter_list = config_global.top_n_stocks_dup['symbol'].to_list()
        config_global.top_n_stocks_dup.set_index('symbol', inplace=True)

        for symbol in iter_list:

            # Print all information
            print('\nSymbol : ', symbol)
            print('-' * 53,
                  '\nTotal number of times stock went up : ', config_global.top_n_stocks_dup[
                      'DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up'][symbol],
                  '\nTotal number of times stock went down : ', config_global.top_n_stocks_dup['DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down'][symbol])
            print('\nTotal number of up trends : ', config_global.top_n_stocks_dup['no_of_up_trend'][symbol],
                  '\nTotal number of down trends : ', config_global.top_n_stocks_dup['no_of_down_trend'][symbol])
            print('\nNumber of times stock went up per up trend :', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend'][symbol],
                  '\ntrend :', config_global.top_n_stocks_dup['trend'][symbol],
                  '\nNumber of times stock went down per down trend :', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend'][symbol])
            print('\nTotal amount increase in each up trend : ', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend'][symbol],
                  '\nTotal amount decrease in each down trend : ', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend'][symbol])
            print('\nAverage amount by which the price went up during up trend : ', config_global.top_n_stocks_dup['DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends'][symbol],
                  '\nAverage amount by which the price went down during down trend : ', config_global.top_n_stocks_dup['DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends'][symbol])
            print('\nAverage number of days during which the price went up : ', config_global.top_n_stocks_dup['DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends'][symbol],
                  '\nAverage number of days during which the price went down : ', config_global.top_n_stocks_dup['DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends'][symbol])
            print('\nAmount change per up and down trend :', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends'][symbol],
                  '\nNumber of days per up and down trend', config_global.top_n_stocks_dup['DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends'][symbol])
            print('\nAverage price in the given period : ',
                  config_global.top_n_stocks_dup['DAY_DATA_IND_STOCK_average_price_input_Period'][symbol])
            print('\nPercent chance : ', config_global.top_n_stocks_dup['computed_percent_chance'][symbol],
                  '\nLast closing price:\t', config_global.top_n_stocks_dup[
                'DAY_DATA_IND_STOCK_last_closing_price'][symbol],
                '\nLast day price change:\t', config_global.top_n_stocks_dup[
                'last_day_price_change'][symbol],
                '\n% change:\t\t', config_global.top_n_stocks_dup['percent_change'][symbol])
            print('-' * 53)
    else:
        print('\nThere are no verbose information to print.')
        sys.exit(0)


def print_stocks_with_high_pc():
    if config_global.all_stock_info.index.size:
        print('\nPrinting stocks with higher percent chance...',
              '\n\nSymbol\t:  Percent Chance')
        config_global.all_stock_info.set_index('symbol', inplace=True)
        for symbol in config_global.all_stock_info.index.to_list():
            print(symbol, '\t: ',
                  config_global.all_stock_info['computed_percent_chance'][symbol])
    else:
        print('\nThere are no stocks with percent chance greater than ',
              config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, '.')
        sys.exit(0)


def print_summary():
    if config_userinput.USER_INPUT_analyze_top_n_csv == 1:
        config_global.top_n_stocks = config_global.all_stock_info
        iter_list = config_global.tickers_list
    else:
        iter_list = config_global.top_n_stocks['symbol'].to_list()

    if config_global.top_n_stocks.index.size:
        print('\nPrinting summary for Top N stocks...')

        config_global.top_n_stocks.set_index('symbol', inplace=True)

        for symbol in iter_list:
            print('\nStock:\t\t\t', symbol,
                  '\nLast closing price:\t', config_global.top_n_stocks[
                      'DAY_DATA_IND_STOCK_last_closing_price'][symbol],
                  '\nLast day price change:\t', config_global.top_n_stocks[
                      'last_day_price_change'][symbol],
                  '\n% change:\t\t', config_global.top_n_stocks['percent_change'][symbol])

        config_print_stock_details.total_gain_percent = config_global.top_n_stocks['percent_change'].mean(
        )
        config_print_stock_details.total_positive_percent_change = sum([1
                                                                        for x in config_global.top_n_stocks['percent_change']
                                                                        if x > 0])
        config_print_stock_details.up_stock_percent = (config_print_stock_details.total_positive_percent_change /
                                                       config_global.top_n_stocks['percent_change'].size)*100
        config_print_stock_details.down_stock_percent = 100 - \
            config_print_stock_details.up_stock_percent

        print('-' * 53,
              '\nTotal gain %:\t\t', config_print_stock_details.total_gain_percent,
              '\nUp stock percent:\t', config_print_stock_details.up_stock_percent,
              '\nDown stock percent:\t', config_print_stock_details.down_stock_percent)
    else:
        print('\nThere are no stocks with percent chance greater than ',
              config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, '.')
        sys.exit(0)
