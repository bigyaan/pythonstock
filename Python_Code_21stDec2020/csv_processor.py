import sys
import pandas as pd

from config import config_global
from config import config_userinput


# Read CSV into a DataFrame
def load_csv():
    config_global.csv_dataframe = pd.read_csv(
        config_global.csv_name, names=['symbols'])
    config_global.tickers_list = config_global.csv_dataframe.symbols.tolist()


def write_csv():
    if config_global.all_stock_info.index.size:
        print('\nWriting CSVs...')

        # Write the symbol list from the dataframe to csv
        config_global.all_stock_info['symbol'].to_csv(
            'symbols_with_greater_percent_chance.csv', index=False, header=False)

        config_global.all_stock_info.sort_values(
            by='computed_percent_chance', ascending=False, inplace=True)

        # Create DataFrame of top n stocks
        # Temporary list of percent chance
        list_of_percent_chance = config_global.all_stock_info['computed_percent_chance'].to_list(
        )

        if len(list_of_percent_chance) <= config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS:
            config_global.top_n_stocks = config_global.all_stock_info.head(
                len(list_of_percent_chance))
        else:
            # Function from this import is only used here
            from math import floor
            count = 0
            # Find N number of stocks excluding repetitions
            for x in range(1, len(list_of_percent_chance)):
                if count == config_userinput.USER_INPUT_NO_OF_TOP_FILTERED_STOCKS:
                    break
                if floor(list_of_percent_chance[x-1]) != floor(list_of_percent_chance[x]):
                    count += 1
            config_global.top_n_stocks = config_global.all_stock_info.head(
                x - 1)

        if config_global.top_n_stocks.index.size:
            # Create CSV for top n stocks
            config_global.top_n_stocks['symbol'].to_csv(
                'top_n_stocks.csv', index=False, header=False)

            if config_userinput.USER_INPUT_write_csv_with_conditions == 'y':
                config_global.top_n_stocks_with_conditions = config_global.top_n_stocks[(
                    config_global.top_n_stocks['MarketCapital'] > config_userinput.USER_INPUT_market_capital)
                    & (config_global.top_n_stocks['fiftyTwoWeeksHigh'] < config_userinput.USER_INPUT_fiftyTwoWeeksHigh)
                    & (config_global.top_n_stocks['fiftyTwoWeeksLow'] > config_userinput.USER_INPUT_fiftyTwoWeeksLow)]

                config_global.top_n_stocks_with_conditions.to_csv(
                    'top_stocks_with applied_conditons.csv', index=False, columns=['symbol', 'MarketCapital', 'fiftyTwoWeeksHigh', 'fiftyTwoWeeksLow'])
        else:
            print('\nThere are no stocks with percent chance greater than ',
                  config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, '.')
            sys.exit(0)
    else:
        print('\nThere are no stocks with percent chance greater than ',
              config_userinput.USER_INPUT_PERCENT_CHANCE_VALUE, '.')
        sys.exit(0)
