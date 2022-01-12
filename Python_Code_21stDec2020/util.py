import os

from config import config_global


def search_csv():
    """
    Search for all CSV files in the working directory and generate a list.
    """
    for root, dirs, files in os.walk('./'):
        config_global.list_of_csv = [
            file for file in files if file.endswith('.csv')]
        break
