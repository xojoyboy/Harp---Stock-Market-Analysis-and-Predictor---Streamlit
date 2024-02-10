import streamlit as st
from models.stock_predictor import StockPredictor

def show_stock_prediction(predictor, future_date):
    """
    This function is used to show the stock prediction for the given stock.
    It gets the stock and its data from app.py and displays the stock prediction using plotly.
    The future date is handled in app.py.
    """
    try:
        predictor.fetch_and_prepare_data("2020-01-01", "2023-12-05")
        predictor.train_model()
        predicted_price = predictor.predict_future_price(future_date)
        st.write(f"The predicted price for {predictor.stock_symbol} on {future_date} is ${predicted_price:.2f}")
    except ValueError as e:
        st.error(f"Error in prediction: {e}")
    