import numpy as np
import pandas as pd
import statistics

def statistical_data(stock_data, symbol):
    """
    Calculates and Prints statistical characteristics of the given stock Symbol.
    """
    symbol = "APPLE" if str.lower(symbol).strip() == 'aapl' else "SAMSUNG"
    # Print statistical data of the stock
    print(f"Statistical Data for the {symbol} Stock:")
    print("-------------------------------")
    print("Summary Statistics:")
    print("-------------------------------")
    mean= np.mean(stock_data['Close'])
    std_dev = np.std(stock_data['Close'])
    min = np.min(stock_data['Close'])
    max = np.max(stock_data['Close'])
    range = stock_data['Close'].max() - stock_data['Close'].min()
    median = statistics.median(stock_data['Close'])
    variance = statistics.variance(stock_data['Close'])
    
    num_of_trading_days = len(stock_data)
    num_of_profit_days = len(stock_data[stock_data["Close"] > stock_data["Open"]])
    num_of_loss_days = len(stock_data[stock_data["Close"] < stock_data["Open"]])

    df = pd.DataFrame([mean, std_dev, min, max, range, median, variance], 
                      index=["Mean", "Standard Deviation", "Min", "Max", "Range", "Median", "Variance"])
    df_additional = pd.DataFrame([num_of_trading_days, num_of_profit_days, num_of_loss_days], 
                                 index=["Number of Trading Days in 2021", "Number of profit days", "Number of loss days"])

    print(df)
    print("Additional Statistics:")
    print("-------------------------------")
    print(df_additional)