import matplotlib.pyplot as plt
import plotly.graph_objs as pplt
import streamlit as st

def visualize_data(stock_data, symbol):
    """
    Visualizes the stock data.
    """
    symbol = "APPLE" if str.lower(symbol).strip() == 'aapl' else "SAMSUNG"
    fig, ax1 = plt.subplots()
    # Plot the open and close prices
    ax1.plot(stock_data['Open'], color='blue', label='Open Price')
    ax1.plot(stock_data['Close'], color='green', label='Close Price')

    # Set the y-axis label for price
    ax1.set_ylabel('Price')

    # Create the volume axis
    ax2 = ax1.twinx()
    ax2.plot(stock_data['Volume'], color='red', label='Volume')

    # Set the y-axis label for volume
    ax2.set_ylabel('Volume')
    # Set the title and legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Rotate and align the x-axis tick labels
    plt.xticks(rotation=45, ha='right')
    
    plt.title('Stock Data ' + symbol)
    plt.show()

def candle_stick_graph(stock_data):
    """
    Visualizes the stock data.
    """
    fig = pplt.Figure(pplt.Candlestick(x=stock_data.index,
                                open=stock_data['Open'],
                                close=stock_data['Close'],
                                high=stock_data['High'],
                                low=stock_data['Low']))
    return fig