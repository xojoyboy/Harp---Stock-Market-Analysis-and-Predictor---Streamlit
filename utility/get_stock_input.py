from models.stock import Stock
from fetching.data_fetcher import get_active_stocks
import streamlit as st

def get_single_stock():
    """
    Display a dropdown to select a single stock. It uses the get_active_stocks() function
    to get the list of all active stocks. The dropdown displays the stock symbol and name.
    The function returns the selected stock.
    Parameters: None
    Returns: dictionary containing the selected stock
    """
    all_stocks = get_active_stocks()
    if not all_stocks:
        st.error("No stock data available.")
        return None

    selected_stock = st.selectbox(
        "Select or type a stock symbol",
        all_stocks,
        format_func=lambda x: f"{x['symbol']} - {x['name']}"
    )

    return selected_stock

def get_multiple_stocks():
    """
    Display a multiselect to select one or more stocks. It uses the get_active_stocks() function
    to get the list of all active stocks. The multiselect displays the stock symbol and name.
    The function returns a list of dictionaries containing the selected stocks.
    Parameters: None
    Returns: list of dictionaries containing the selected stocks
    """
    all_stocks = get_active_stocks()
    if not all_stocks:
        st.error("No stock data available.")
        return []

    selected_stocks = st.multiselect(
        "Select one or more stock symbols",
        all_stocks,
        format_func=lambda x: f"{x['symbol']} - {x['name']}"
    )

    return selected_stocks


