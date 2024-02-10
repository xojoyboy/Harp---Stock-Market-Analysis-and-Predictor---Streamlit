from alpha_vantage.timeseries import TimeSeries
import streamlit as st
import pandas as pd

ALPHA_VANTAGE_API_KEY = "E9GT7672W4Z5US5G"

@st.cache_data
def get_stock_data(symbol, start_date, end_date):
    """
    Fetches stock data from Alpha Vantage API. It returns a pandas DataFrame with the stock data.

    Parameters: symbol (str): The stock symbol for which the data is to be fetched.
                start_date (str): The start date from which the data is to be fetched.
                end_date (str): The end date till which the data is to be fetched.
    Returns: pandas DataFrame with the stock data in the following format:
            Date, Open, High, Low, Close, Volume
    Errors: If any error occurs, an empty DataFrame is returned.
            An error message is also displayed using st.error()
    """
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    try:
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        data.index = pd.to_datetime(data.index)
        # Filter based on passed start and end dates
        filtered_data = data[(data.index >= pd.to_datetime(start_date)) & (data.index <= pd.to_datetime(end_date))]
        return filtered_data
    except Exception as e:
        st.error(f"Failed to fetch stock data: {e}")
        return pd.DataFrame()

@st.cache_data
def get_active_stocks():
    """
    Fetches list of active stocks from Alpha Vantage API and returns a list of dictionaries with
    symbol and name of the stock.

    Parameters: None
    Returns: List of dictionaries with symbol and name of the stock.
    Errors: If any error occurs, an empty list is returned.
            An error message is also displayed using st.error()
    """
    csv_url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={ALPHA_VANTAGE_API_KEY}'
    try:
        # Use pandas to directly read the CSV from the URL
        raw_stocks_dataframe = pd.read_csv(csv_url)
        
        # Turn DataFrame to a list of dictionaries
        stocks = raw_stocks_dataframe[['symbol', 'name']].to_dict(orient='records')
        
        return stocks
    except Exception as e:
        st.error(f"Failed to fetch stock symbols: {e}")
        return []

