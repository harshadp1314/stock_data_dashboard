import streamlit as st
import pandas as pd
# import plotly.graph_objs as pplt
import matplotlib.pyplot as plt
from stocknews import StockNews

from DSSC_FC_MVP_Timeseries_Forcasting import prophet
from DSCC_FP_MVP_Visualization import candle_stick_graph
from DSSC_FC_MVP_Timeseries_Analysis import moving_avearges, exponential_Smoothing
from DSCC_FP_MVP_Storage import retrieve_data_from_s3
from DSSC_FC_MVP_Timeseries_Forcasting import prophet

st.button(":apple: Apple Stock")
stock_data_analysis, forecasting_tab = st.tabs(["Stock Data Analysis", "Forecasting"])

with stock_data_analysis:

    st.title("""Stock Data Dashboard""")

    analysis_dashboard = st.sidebar.container()
    analysis_dashboard.markdown('User Input')
    # window_selection_c = st.sidebar.container() # create an empty container in the sidebar
    # sub_columns = window_selection_c.columns(2) #Split the container into two columns for start and end date

    def get_input():
        stock_symbol = analysis_dashboard.selectbox("Stock Symbol", ("Apple", "Samsung"))
        start_date = analysis_dashboard.text_input("Start Date", "2021-01-01")
        end_date = analysis_dashboard.text_input("End Date", "2021-12-31")
        chart_type = analysis_dashboard.selectbox("Chart Type", ("Line Pattern", "Candle Stick Pattern"))
        indicator = analysis_dashboard.selectbox("Indicators", ("Select an Indicator","Moving Averages", "Exponential Smoothing"))
        # forecasting = analysis_dashboard.selectbox("Forecasting", ("None", "Arima","Prophet"))

        return start_date, end_date, stock_symbol, chart_type, indicator
    
    @st.cache_data
    def get_data(symbol, start, end):
        if symbol == 'Apple':
            df = retrieve_data_from_s3('apple_stock')
        elif symbol == 'Samsung':
            df = retrieve_data_from_s3('samsung_stock')
        else:
            df = pd.DataFrame(columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])

        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        start_row = 0
        end_row = 0

        for i in range(0, len(df)):
            if start <= pd.to_datetime(df['Date'][i]):
                start_row = i
                break

        for j in range(0, len(df)):
            if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
                end_row = len(df) -1 -j
                break
        
        df = df.set_index(pd.DatetimeIndex(df['Date'].values))

        return df.iloc[start_row:end_row+1, :]

    start, end, symbol, chart_type, indicator = get_input()

    df = get_data(symbol, start, end)
    
    if chart_type == "Line Pattern"and indicator == "Select an Indicator":
        st.header(symbol+" Open Price\n")
        st.line_chart(df['Open'])
        
        st.header(symbol+" Close Price\n")
        st.line_chart(df['Close'])

        st.header(symbol+" Volume\n")
        st.line_chart(df['Volume'])  

    if chart_type == "Line Pattern"and indicator == "Moving Averages":
        st.header(symbol+" Open Price\n")
        ma = moving_avearges(df)
        st.line_chart(ma['MA5'])
        
        # st.header(symbol+" Close Price\n")
        # st.line_chart(df['Close'])
        # # ma = moving_avearges(df)
        # # st.pyplot(ma)

        # st.header(symbol+" Volume\n")
        # st.line_chart(df['Volume'])     
    
    elif chart_type == "Candle Stick Pattern" and indicator == "Select an Indicator":
        st.write("Indicator Inprogress")
        fig = candle_stick_graph(df)
        st.plotly_chart(fig)

    elif indicator == "Select an Indicator":
        st.write("Please Select an Indicator")

    pricing_data, statistical_data, news = st.tabs(["Pricing Data", "Statistical Data", "Top 10 News"])

    with pricing_data:
        st.header("Stock Data")
        st.write(df)
    with statistical_data:
        st.header("Data Statistics")
        st.write(df.describe())
    with news:
        st.header(f'News of {symbol}')
        sn = StockNews(symbol, save_news=False)
        df_news = sn.read_rss()
        for i in range(10):
            st.subheader(f'News {i+1}')
            st.write(df_news['published'][i])
            st.write(df_news['title'][i])
            st.write(df_news['summary'][i])
            title_sentiment = df_news['sentiment_title'][i]
            st.write(f'Title Sentiment {title_sentiment}')
            news_sentiment = df_news['sentiment_summary'][i]
            st.write(f'News Sentiment {news_sentiment}')

with forecasting_tab:
    st.title("""Stock Data Forecast Using Prophet""")

    if "TEST_INTERVAL_LENGTH" not in st.session_state:
    # set the initial default value of test interval
        st.session_state.TEST_INTERVAL_LENGTH = 60

    if "TRAIN_INTERVAL_LENGTH" not in st.session_state:
        # set the initial default value of the training length widget
        st.session_state.TRAIN_INTERVAL_LENGTH = 500

    if "HORIZON" not in st.session_state:
        # set the initial default value of horizon length widget
        st.session_state.HORIZON = 60

    #---------------------------------------------------------Train_test_forecast_splits---------------------------------------------------
    st.sidebar.markdown("## Forecasts")
    train_test_forecast_c = st.sidebar.container()

    train_test_forecast_c.markdown("## Select interval lengths")

    HORIZON = train_test_forecast_c.number_input(
        "Inference horizon", min_value=7, max_value=200, key="HORIZON"
    )
    TEST_INTERVAL_LENGTH = train_test_forecast_c.number_input(
        "number of days to test on and visualize",   
        min_value=7,
        key="TEST_INTERVAL_LENGTH",
    )

    TRAIN_INTERVAL_LENGTH = train_test_forecast_c.number_input(
        "number of  day to use for training",
        min_value=60,
        key="TRAIN_INTERVAL_LENGTH",
    )


    train_test_forecast_c.button(
        label="Train",
        key='TRAIN_JOB'
    )
    """
    part-3
    Calling a static method in the Stock class to create a stock object, train prophet,test , forecast and plot. 
    It's behavior depends on the session_state variables  linked to the widgets above. 
    """
    forecast = prophet(df)
    st.dataframe(df.tail())
    st.subheader("Stock Price Forecast")
    st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    # st.pyplot(forecast)
    # Stock.train_test_forecast_report(SYMB)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(forecast['ds'].values, forecast['yhat'].values, color='blue', label='Forecast')
    # ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=0.5)
    ax.plot(df.index.values, df['Close'].values, color='red', label='Actual')
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.set_title('Stock Price Forecast')
    ax.legend()
    st.pyplot(fig)

    # @staticmethod
    # def train_test_forecast_report(symb): 
    #     """Launch training and plot testing results and reports MAPE error, finally it plots forecasts up to the specified horizon"""
    #     if st.session_state.TRAIN_JOB or st.session_state.TRAINED:
    #         text=st.empty() # Because streamlit adds widgets sequentially, we have to reserve a place at the top (after the chart of part 1)
    #         bar=st.empty() # Reserve a place for a progess bar
            
    #         text.write('Training model ... ') 
    #         bar=st.progress(0)

    #         stock = Stock(symb) 
    #         bar.progress(10)
    #         TEST_INTERVAL_LENGTH=st.session_state.TEST_INTERVAL_LENGTH #Retrieve input from the user
    #         TRAIN_INTERVAL_LENGTH=st.session_state.TRAIN_INTERVAL_LENGTH

    #         stock.load_train_test_data(TEST_INTERVAL_LENGTH, TRAIN_INTERVAL_LENGTH) #load train test data into the stock object, it's using cache
    #         bar.progress(30)
    #         stock.train_prophet() #this is also using cache
    #         bar.progress(70)
    #         text.write('Plotting test results ...')
    #         fig = stock.plot_test()
    #         bar.progress(100)
    #         bar.empty() #Turn the progress bar object back to what it was before and empty container
    #         st.markdown(
    #             f"## {symb} stock forecasts on testing set, Testing error {round(stock.test_mape*100,2)}%"
    #         )
    #         st.plotly_chart(fig)
    #         text.write('Generating forecasts ... ')
    #         fig2=stock.plot_inference() #Generate forecasts and plot them (no cache but figures are not updated if their data didn't change)
    #         st.markdown(f'## Forecasts for the next {st.session_state.HORIZON} days')
    #         st.plotly_chart(fig2)
    #         text.empty()
    #         """The button click will trigger this code to run only once, 
    #            the following flag TRAINED will keep this block of code executing even after the click,
    #            it won't redo everything however because we are using cache. 
    #            this flag needs to be initialized to False in the session state in main.py before the button"""

    #         st.session_state.TRAINED=True 
    #     else:
    #         st.markdown('Setup training job and hit Train')



    