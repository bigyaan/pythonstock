import yfinance as yf
import pandas as pd

from config import config_global
from config import config_userinput
from config import config_compute_engine


# Check if there was an up trend
def is_price_up():
    """
    This function checks if the price of the stock had rose before the current drop in price.
    The uptrend is only recorded after detecting a drop in price.
    Therefore, this function is only called when the stock price drops.
    """
    # Following variable represents the no of times price had risen before a drop.
    # So an up trend is considered if the stock price had risen
    if config_global.days_count_for_up_trend:
        # Store total days for this up trend
        config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend.append(
            config_global.days_count_for_up_trend)
        config_global.trend.append(config_global.days_count_for_up_trend)   
        # Store amount changed for this up trend
        config_global.DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend.append(
            sum(config_global.LIST_amount_change_per_uptrend))
        # Clearing for another trend
        config_global.LIST_amount_change_per_uptrend = []
        # Store number of times stock went up
        config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up += config_global.days_count_for_up_trend
        # Clearing for another trend
        config_global.days_count_for_up_trend = 0

        # This flags the end of an up trend and start of a down trend
        config_compute_engine.was_downtrend = 1
        return 1
    else:
        return 0


# Check if there was a down trend
def is_price_down():
    """
    This function checks if the price of the stock had dropped before the current rise in price.
    The downtrend is only recorded after detecting a rise in price.
    Therefore, this function is only called when the stock price rises.
    """
    # Following variable represents the no of times price had dropped before a rise.
    # So a down trend is considered if the stock price had dropped
    if config_global.days_count_for_down_trend:
        # Store total days for this down trend
        config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend.append(
            config_global.days_count_for_down_trend)
        config_global.trend.append(-config_global.days_count_for_down_trend)    
        # Store amount changed for this down trend
        config_global.DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend.append(
            sum(config_global.LIST_amount_change_per_downtrend))
        # Clearing for another trend
        config_global.LIST_amount_change_per_downtrend = []
        # Store number of times stock went down
        config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down += config_global.days_count_for_down_trend
        # Clearing for another trend
        config_global.days_count_for_down_trend = 0

        # This flags the end of down trend and start of up trend
        config_compute_engine.was_uptrend = 1
        return 1
    else:
        return 0


# Check for up and down trend
def is_updown_trend():
    """
    This function checks for up and down trend.
    If both was_uptrend and was_ downtrend variables are 1, it is an up and down trend.
    """
    if config_compute_engine.was_uptrend and config_compute_engine.was_downtrend:
        # Store amount change for up and down trend
        # Adding because the amount is stored as negative values for down trend
        config_global.DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends.append(
            config_global.DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend[-1] +
            config_global.DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend[-1]
        )
        # Clear if an up and down trend was detected
        config_compute_engine.was_uptrend = config_compute_engine.was_downtrend = 0
        # Store total number of days in up and down trend
        config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends.append(
            config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend[-1] +
            config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend[-1]
        )


def all_operation():
    """
    This function is split only to be used both by the single stock and the multiple stocks.
    """
    # Clear all variables before analyzing every stock symbol
    config_global.days_count_for_up_trend = 0
    config_global.days_count_for_down_trend = 0

    config_global.LIST_amount_change_per_uptrend = []
    config_global.LIST_amount_change_per_downtrend = []

    config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend = []
    config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend = []

    config_global.DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend = []
    config_global.DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend = []

    config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up = 0
    config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down = 0

    config_compute_engine.was_downtrend = 0
    config_compute_engine.was_uptrend = 0

    config_global.DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends = []
    config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends = []

    config_global.no_of_up_trend = 0
    config_global.no_of_down_trend = 0

    config_global.DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends = 0
    config_global.DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends = 0

    config_global.DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends = 0
    config_global.DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends = 0

    config_global.DAY_DATA_IND_STOCK_last_closing_price = 0
    config_global.DAY_DATA_IND_STOCK_average_price_input_Period = 0

    config_global.last_day_price_change = 0.0
    config_global.percent_change = 0.0

    config_global.uptrend_flag = 0
    config_global.trend =[]

    # Process closing price list for current symmbol
    for index in range(1, len(config_global.closing_prices_list)):
        previous_price = config_global.closing_prices_list[index-1]
        current_price = config_global.closing_prices_list[index]

        if (current_price > previous_price):
            # Count number of days stock price goes up
            config_global.days_count_for_up_trend += 1
            # Store amount difference for up trend
            config_global.LIST_amount_change_per_uptrend.append(
                current_price - previous_price)
            # Check if there was a down trend
            is_price_down()
        else:
            # Count number of days stock price goes down
            config_global.days_count_for_down_trend += 1
            # Store amount difference for down trend
            config_global.LIST_amount_change_per_downtrend.append(
                current_price - previous_price)
            # Check if there was an up trend
            is_price_up()

        # Check for up and down trend
        is_updown_trend()

    # Trends are only recorded after a break.
    # So, the following 3 calls are to check for the last change.
    if is_price_up():
        # This flag is used to represent the start of an up trend.
        # Used when deciding to compute the percent chance.
        config_global.uptrend_flag = 1 if config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend[
            -1] == 1 else 0
    else:
        is_price_down()

    # Check for up and down trend
    is_updown_trend()

    # Number of up trend = Length of list of number of days price went up per up trend
    config_global.no_of_up_trend = len(
        config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend)
    # Number of down trend = Length of list of number of days price went down per down trend
    config_global.no_of_down_trend = len(
        config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend)

    # If there are no up trends, will result in a zero division error
    if config_global.no_of_up_trend:
        # Average up amount in up trends = sum of list of amount per up trend / total up trend
        config_global.DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends = sum(
            config_global.DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend) / config_global.no_of_up_trend

        # Average number of days in up trends = total days stock went up / number of up trends
        config_global.DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends = config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up / \
            config_global.no_of_up_trend
    else:
        config_global.DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends = 0
        config_global.DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends = 0

    # If there are no down trends, will result in a zero division error
    if config_global.no_of_down_trend:
        # Average down amount in down trends = sum of list of amount per down trend / total down trend
        config_global.DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends = sum(
            config_global.DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend) / config_global.no_of_down_trend

        # Average number of days in down trends = total days stock went down / number of down trends
        config_global.DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends = config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down / \
            config_global.no_of_down_trend
    else:
        config_global.DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends = 0
        config_global.DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends = 0

    # Total days = length of list of closing prices
    total_days = len(config_global.closing_prices_list)

    # Last closing price = last item of closing prices list
    config_global.DAY_DATA_IND_STOCK_last_closing_price = config_global.closing_prices_list[
        total_days - 1]

    config_global.last_day_price_change = current_price - previous_price

    config_global.percent_change = (
        config_global.last_day_price_change/previous_price)*100

    # Average price in given period = total of closing prices list / total days
    config_global.DAY_DATA_IND_STOCK_average_price_input_Period = sum(
        config_global.closing_prices_list)/total_days

    # Store all computed information in a dataframe
    config_global.all_stock_info = config_global.all_stock_info.append({'symbol': config_global.symbol,
                                                                        'total_days': total_days,
                                                                        'DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up': config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up,
                                                                        'DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down': config_global.DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down,
                                                                        'no_of_up_trend': config_global.no_of_up_trend,
                                                                        'no_of_down_trend': config_global.no_of_down_trend,
                                                                        'DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend': config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend,
                                                                        'trend': config_global.trend,
                                                                        'DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend': config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend,
                                                                        'DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend': config_global.DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend,
                                                                        'DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend': config_global.DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend,
                                                                        'DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends': config_global.DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends,
                                                                        'DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends': config_global.DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends,
                                                                        'DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends': config_global.DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends,
                                                                        'DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends': config_global.DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends,
                                                                        'DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends': config_global.DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends,
                                                                        'DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends': config_global.DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends,
                                                                        'DAY_DATA_IND_STOCK_last_closing_price': config_global.DAY_DATA_IND_STOCK_last_closing_price,
                                                                        'last_day_price_change': config_global.last_day_price_change,
                                                                        'percent_change': config_global.percent_change,
                                                                        'DAY_DATA_IND_STOCK_average_price_input_Period': config_global.DAY_DATA_IND_STOCK_average_price_input_Period,
                                                                        'uptrend_flag': config_global.uptrend_flag
                                                                        }, ignore_index=True)


def compute(singleStock=False):
    """
    Downloads data with yfinance for all stocks and generates all parameters required by filters.
    This function is shared between the single and multiple stocks to reuse the existing variables.
    """
    if singleStock:
        all_operation()
    else:
        print('\nRetrieving data...')
        # Download data for all symbols in the CSV
        data = yf.download(config_global.tickers_list, start=config_userinput.USER_INPUT_start_date,
                           end=config_userinput.USER_INPUT_end_date, group_by='ticker')

        # Remove all columns that has no data
        data.dropna(axis=1, inplace=True)

        # Prevent crash when the list only contains one symbol
        if isinstance(data.columns, pd.MultiIndex):
            # Remove unused levels from the dataframe
            data.columns = data.columns.remove_unused_levels()

            # Update the tickers list
            config_global.tickers_list = list(data.columns.levels[0])

        # This is only to prevent auto-sorting of the columns in the dataframe, not necessary
        config_global.all_stock_info = pd.DataFrame(columns=['symbol',
                                                             'total_days',
                                                             # ALl of the following are required for printing information
                                                             #  Some are used in percent chance calculation
                                                             'DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_up',
                                                             'DAY_DATA_ALL_IND_STOCK_no_of_times_price_went_down',
                                                             'no_of_up_trend',
                                                             'no_of_down_trend',
                                                             'DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_up_per_up_trend',
                                                             'DAY_DATA_LIST_IND_STOCK_no_of_days_price_went_down_per_down_trend',
                                                             'DAY_DATA_LIST_IND_STOCK_total_up_amount_per_up_trend',
                                                             'DAY_DATA_LIST_IND_STOCK_total_down_amount_per_down_trend',
                                                             'DAY_DATA_ALL_IND_STOCK_average_up_amount_in_up_trends',
                                                             'DAY_DATA_ALL_IND_STOCK_average_down_amount_in_down_trends',
                                                             'DAY_DATA_ALL_IND_STOCK_average_up_days_in_up_trends',
                                                             'DAY_DATA_ALL_IND_STOCK_average_down_days_in_down_trends',
                                                             'DAY_DATA_LIST_IND_STOCK_amount_change_per_up_and_down_trends',
                                                             'DAY_DATA_LIST_IND_STOCK_no_of_days_per_up_and_down_trends',
                                                             'DAY_DATA_IND_STOCK_last_closing_price',
                                                             'last_day_price_change',
                                                             'percent_change',
                                                             'DAY_DATA_IND_STOCK_average_price_input_Period',
                                                             'uptrend_flag',
                                                             'computed_percent_chance'])

        print('\nPerforming calculations...')

        for config_global.symbol in config_global.tickers_list:
            # Create a list of closing prices for each symbol
            config_global.closing_prices_list = data[config_global.symbol]['Close'].tolist(
            )
            # Carry out all operations
            all_operation()
