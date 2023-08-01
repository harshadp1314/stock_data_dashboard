import matplotlib.pyplot as plt
# from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
# from pmdarima.arima import auto_arima
# from statsmodels.tsa.arima.model import ARIMA
from DSCC_FP_MVP_Storage import retrieve_data_from_s3

apple_df = retrieve_data_from_s3('apple_stock')
# samsung_df = retrieve_data_from_s3('samsung_stock')

def moving_avearges(df):
    
    df = df[['Date', 'Close']].copy()

    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA14'] = df['Close'].rolling(window=14).mean()
    df['EMA'] = df['Close'].ewm(span=30).mean()

    # print(df)

    # df = df[['Close', 'MA5', 'MA14', 'EMA']].plot(label='Moving Average with EMA', figsize = (16, 8), xlabel='Moving Average', ylabel='Stock Price')

    return df

def exponential_Smoothing(df):
    span = 3

    alpha = 2/(span+1)

    df['ES3'] = SimpleExpSmoothing(df['Open']).fit(smoothing_level= alpha, optimized=False).fittedvalues.shift(-1)
    df[['Open', 'ES3', 'Date']].plot(figsize=(15,6))
    plt.show()

moving_avearges(apple_df)
