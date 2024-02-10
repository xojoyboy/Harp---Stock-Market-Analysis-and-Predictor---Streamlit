import streamlit as st
import plotly.graph_objs as go
from models.stock import Stock

def show(stock):
    """
    This function is used to show the trend visualization for a given stock.
    the stock and its data are passed from app.py and the trend visualization is displayed using plotly.
    The date range is also handled in app.py.
    The trend updates dynamically based on the user's selections that are handled in app.py.
    """
    st.title("Trend Visualization")

    if not stock or stock.data.empty:
        st.error("No stock data available. Please select a stock.")
        return

    # User option for displaying SMA
    show_sma = st.checkbox("Show Simple Moving Average")
    sma_window = st.number_input("SMA Window", min_value=1, max_value=100, value=20, step=1) if show_sma else None

    # If user opted to show SMA, calculate it
    if show_sma:
        stock.calculate_sma(sma_window)

    fig = go.Figure()

    # Plotting the stock's close price
    fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['4. close'], mode='lines', name='Close Price'))

    # Plotting SMA if selected
    if show_sma:
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data[f'SMA_{sma_window}'], mode='lines', name=f'SMA {sma_window}'))

    fig.update_layout(title=f'Stock Price for {stock.symbol}', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)
