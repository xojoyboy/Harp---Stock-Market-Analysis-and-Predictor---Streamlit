import streamlit as st
import plotly.graph_objs as go
from models.stock import Stock

def show(stock):
    """
    This function is used to show the market indicator analysis for the given stock.
    It gets the stock and its data from app.py and displays the market indicator analysis using plotly.
    The market indicators are calculated using the Stock object.

    The visuals are updated based on the user's selection of the indicators to show, window sizes,
    and date range which is handled in app.py.
    """
    st.title("Market Indicator Analysis")

    if not stock or stock.data.empty:
        st.error("No stock data available for analysis.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['4. close'], mode='lines', name='Close Price'))

    col1, col2, col3 = st.columns(3)
    with col1:
        show_sma = st.checkbox("Show SMA")
        show_ema = st.checkbox("Show EMA")
    with col2:
        show_rsi = st.checkbox("Show RSI")
        show_macd = st.checkbox("Show MACD")
    with col3:
        show_bb = st.checkbox("Show Bollinger Bands")

    # Simple Moving Average
    if show_sma:
        sma_window = st.number_input("SMA Window Size", min_value=1, max_value=100, value=20)
        stock.calculate_sma(sma_window)
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data[f'SMA_{sma_window}'], mode='lines', name=f'SMA {sma_window}'))

    # Exponential Moving Average
    if show_ema:
        ema_window = st.number_input("EMA Window Size", min_value=1, max_value=100, value=20)
        stock.calculate_ema(ema_window)
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data[f'EMA_{ema_window}'], mode='lines', name=f'EMA {ema_window}'))

    # Relative Strength Index
    if show_rsi:
        rsi_window = st.number_input("RSI Window Size", min_value=1, max_value=100, value=14)
        stock.calculate_rsi(rsi_window)
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['RSI'], mode='lines', name='RSI'))

    # Moving Average Convergence Divergence
    if show_macd:
        short_window = st.number_input("MACD Short Window", min_value=1, max_value=50, value=12)
        long_window = st.number_input("MACD Long Window", min_value=1, max_value=50, value=26)
        stock.calculate_mov_avg_convergence_divergence(short_window, long_window)
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['MACD'], mode='lines', name='MACD'))
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['Signal'], mode='lines', name='Signal'))

    # Bollinger Bands
    if show_bb:
        bb_window = st.number_input("Bollinger Bands Window Size", min_value=1, max_value=100, value=20)
        stock.calculate_bollinger_bands(bb_window)
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['Upper Band'], mode='lines', name='Upper Bollinger Band'))
        fig.add_trace(go.Scatter(x=stock.data.index, y=stock.data['Lower Band'], mode='lines', name='Lower Bollinger Band'))

    fig.update_layout(title=f'Market Indicators for {stock.symbol}', xaxis_title='Date', yaxis_title='Price and Indicators')
    st.plotly_chart(fig)
