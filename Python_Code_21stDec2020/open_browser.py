import webbrowser

from config import config_global


def open_in_tabs(list_of_symbols):
    for symbol in list_of_symbols:
        webbrowser.open_new_tab(
            'https://finance.yahoo.com/quote/{}'.format(symbol))
        webbrowser.open_new_tab(
            'https://finance.yahoo.com/chart/{}'.format(symbol))
        webbrowser.open_new_tab(
            'https://finance.yahoo.com/quote/{}/history'.format(symbol))
