from prophet import Prophet
from DSCC_FP_MVP_Storage import retrieve_data_from_s3

def prophet(df):
    df = df.reset_index()
    df = df[['Date', 'Close']].copy()
    # df = df.reset_index(drop=True)

    df = df.rename(columns = {'Date' : 'ds', 'Close' : 'y'})
    # return df_1.head()

    m = Prophet()
    m.fit(df)
    future_price = m.make_future_dataframe(periods=7)
    forecast = m.predict(future_price)
    # return forecast
    # return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    
    # plot the forecasts
    # fig = m.plot(forecast)
    
    # # plot the components 
    # fig2 = m.plot_components(forecast)
    
    return forecast

