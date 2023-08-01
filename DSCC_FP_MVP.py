import yfinance as yf
import pandas as pd
from DSCC_FP_MVP_Storage import store_df_into_s3, retrieve_data_from_s3
from DSCC_FP_MVP_StatisticalAnalysis import statistical_data
from DSCC_FP_MVP_Visualization import visualize_data, candle_stick_graph
from DSSC_FC_MVP_InteractiveVisualization import interactive_dashboard

apple = 'aapl'
samsung = '005930.KS'

def fetch_stock_data(stock_tickerSymbol):

    # Define the start and end dates of the stocks
    start_date = '2021-01-01'
    end_date = '2021-12-31'

    # Get the data for the stocks
    stock_data = yf.download(stock_tickerSymbol, start=start_date, end=end_date, period='15m')

    stock_data.reset_index(inplace=True)

    # stock_data['Date'] = stock_data['Date'].dt.strftime('%Y/%m/%d')

    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    stock_data['Month'] = stock_data['Date'].dt.month

    # Store the data in a pandas dataframe
    df_stock_data = pd.DataFrame(stock_data)
    
    return df_stock_data

# Fetchs the stock data from yfinance and store in a dataframe.
# df_apple = fetch_stock_data(apple)
# df_samsung = fetch_stock_data(samsung)

# # Store the data in AWS S3
# store_df_into_s3(df_apple, 'apple_stock')
# store_df_into_s3(df_samsung, 'samsung_stock')

# apple_df = retrieve_data_from_s3('apple_stock')
# samsung_df = retrieve_data_from_s3('samsung_stock')

# calculates stock data statistics and display as a dataframe.
# statistical_data(df_apple, apple)
# statistical_data(df_samsung, samsung)

# # Displays line graphs of each stock data with 'Open', 'Close' and 'Volume' data.
# visualize_data(df_apple, 'aapl')
# visualize_data(df_samsung, 'samsung')

# # Displays candle stick pattern of the stock data using plotly.
# candle_stick_graph(df_apple, 'aapl')
# candle_stick_graph(df_samsung, 'samsung')

# interactive_dashboard()

# moving_averages(df_apple)


