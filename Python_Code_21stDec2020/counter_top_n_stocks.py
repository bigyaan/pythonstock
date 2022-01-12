import pandas as pd

def counter2():
    results = pd.read_csv('top_n_stocks.csv')
    return(len(results))