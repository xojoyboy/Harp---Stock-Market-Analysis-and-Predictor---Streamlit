import streamlit as st
import plotly.graph_objs as go
from models.stock import Stock
import pandas as pd

def show(stocks):
    """
    This app compares the performance of the selected stocks. The list of stock objects and 
    their data are passed from app.py and the comparison is displayed using plotly.
    """
    st.title("Stock Comparison")

    if not stocks:
        st.error("No stocks selected for comparison.")
        return

    fig = go.Figure()

    for stock in stocks:
        if stock.data.empty:
            st.error(f"No data available for stock: {stock.symbol}.")
            continue

        # Normalize the data to compare the stock returns
        normalized_data = (stock.data['4. close'] / stock.data['4. close'].iloc[0]) * 100
        fig.add_trace(go.Scatter(x=stock.data.index, y=normalized_data, mode='lines', name=stock.symbol))

    fig.update_layout(title='Stock Performance Comparison', xaxis_title='Date', yaxis_title='Normalized Price')
    st.plotly_chart(fig)
