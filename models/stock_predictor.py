import numpy as np
from sklearn.linear_model import LinearRegression
from fetching.data_fetcher import get_stock_data  
import pandas as pd

class StockPredictor:
    """
    This class is used to predict future stock prices. It uses the LinearRegression model from sklearn.
    It uses the get_stock_data() function from fetching/data_fetcher.py to fetch the stock data that is used to train the model.
    It uses the LinearRegression model to train the model and predict the future stock price.

    You can use this class as follows:
    predictor = StockPredictor("MSFT")
    predictor.fetch_and_prepare_data("2020-01-01", "2023-12-05")
    predictor.train_model()
    predicted_price = predictor.predict_future_price("2024-01-01")

    Learn more about LinearRegression here:
    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
    """
    def __init__(self, stock_symbol):
        if not stock_symbol or not isinstance(stock_symbol, str):
            raise ValueError("Stock symbol must be a non-empty string")
        self.stock_symbol = stock_symbol
        self.model = LinearRegression()
        self.data = None

    def fetch_and_prepare_data(self, start_date, end_date):
        """
        This method fetches the stock data and prepares it for training the model.
        """
        if not start_date or not end_date:
            raise ValueError("Start and end dates must be provided")
        self.data = get_stock_data(self.stock_symbol, start_date, end_date)
        self.data = self.data.sort_index(ascending=True)
        self.data.index = pd.to_datetime(self.data.index)
        self.data['DateNum'] = (self.data.index - self.data.index.min()).days

    def train_model(self):
        """
        This method trains the model using the stock data.
        """
        if self.data is not None and '4. close' in self.data.columns:
            X = self.data[['DateNum']]
            y = self.data['4. close']
            self.model.fit(X, y)
        else:
            raise ValueError("Data not available or '4. close' column missing.")

    def predict_future_price(self, future_date):
            """
            This method predicts the future stock price for the given date.
            """
            future_date_num = (pd.to_datetime(future_date) - self.data.index.min()).days
            return self.model.predict([[future_date_num]])[0]
