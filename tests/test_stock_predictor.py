"""
Very hard to test the stock class due to its dependency on the AlphaVantage API.
The data returned from the API is not static and changes over time.
Prediction using regression on stock data is also not very accurate and the dataframe
returned from API varies a lot over time.

Can only test the StockPredictor class by mocking the get_stock_data function.
Moreover, testing is better done by comparing the results of the prediction with
the actual stock price in the future.
"""
import sys
sys.path.append('C:\\Users\\slaye\\OneDrive\\Desktop\\NEU\\5001\\Final Project\\Harp')
import unittest
from unittest.mock import patch
from models.stock_predictor import StockPredictor
import pandas as pd
import numpy as np

def get_stock_data_mock(symbol, start_date, end_date):
    index = pd.date_range(start=start_date, periods=10, freq='D')
    data = pd.DataFrame({
        '1. open': np.random.rand(10),
        '2. high': np.random.rand(10),
        '3. low': np.random.rand(10),
        '4. close': np.linspace(100, 190, 10),
        '5. volume': np.random.randint(100000, 1000000, 10)
    }, index=index)
    data.index.name = 'date'
    return data

class TestStockPredictor(unittest.TestCase):
    @patch('models.stock_predictor.get_stock_data', side_effect=get_stock_data_mock)
    def test_fetch_and_prepare_data(self, mock_get_stock_data):
        predictor = StockPredictor('AAPL')
        predictor.fetch_and_prepare_data('2020-01-01', '2020-01-10')
        self.assertFalse(predictor.data.empty)

    @patch('models.stock_predictor.get_stock_data', side_effect=get_stock_data_mock)
    def test_train_model(self, mock_get_stock_data):
        predictor = StockPredictor('AAPL')
        predictor.fetch_and_prepare_data('2020-01-01', '2020-01-10')
        predictor.train_model()
        self.assertIsNotNone(predictor.model.coef_)

    def test_train_model_no_data(self):
        predictor = StockPredictor('AAPL')
        predictor.data = None  
        with self.assertRaises(ValueError):
            predictor.train_model()

    @patch('models.stock_predictor.get_stock_data', side_effect=get_stock_data_mock)
    def test_predict_future_price(self, mock_get_stock_data):
        predictor = StockPredictor('AAPL')
        predictor.fetch_and_prepare_data('2020-01-01', '2020-01-10')
        predictor.train_model()
        future_price = predictor.predict_future_price('2020-01-15')
        self.assertIsInstance(future_price, float)

if __name__ == '__main__':
    unittest.main()
