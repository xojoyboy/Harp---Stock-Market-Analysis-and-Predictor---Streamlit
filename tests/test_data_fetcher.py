import sys
sys.path.append('C:\\Users\\slaye\\OneDrive\\Desktop\\NEU\\5001\\Final Project')
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from fetching import data_fetcher

class TestDataFetcher(unittest.TestCase):

    def setUp(self):
        # Sample stock data for testing
        self.sample_stock_data = pd.DataFrame({
            '4. close': [150.75, 153.31],
            '5. volume': [100500, 110200]
        }, index=pd.to_datetime(['2020-01-01', '2020-01-02']))

    @patch('data.data_fetcher.TimeSeries')
    def test_get_stock_data_successful(self, mock_ts):
        # Mocking the TimeSeries class from alpha_vantage
        mock_ts_instance = mock_ts.return_value
        mock_ts_instance.get_daily.return_value = (self.sample_stock_data, None)

        symbol = 'AAPL'
        start_date = '2020-01-01'
        end_date = '2020-01-02'
        response = data_fetcher.get_stock_data(symbol, start_date, end_date)

        # Check if response matches the sample data
        pd.testing.assert_frame_equal(response, self.sample_stock_data)

    @patch('data.data_fetcher.requests.Session')
    def test_get_active_stocks_successful(self, mock_session):
        # Mock the requests.Session.get call to return a successful response
        mock_response = MagicMock()
        mock_response.content.decode.return_value = "symbol,name\nAAPL,Apple Inc.\nMSFT,Microsoft Corporation"
        mock_session.return_value.__enter__.return_value.get.return_value = mock_response

        response = data_fetcher.get_active_stocks()

        expected_stocks = [{'symbol': 'AAPL', 'name': 'Apple Inc.'}, {'symbol': 'MSFT', 'name': 'Microsoft Corporation'}]

        self.assertEqual(response, expected_stocks)

    @patch('data.data_fetcher.TimeSeries')
    def test_get_stock_data_unsuccessful(self, mock_ts):
        # Simulating an exception in the TimeSeries.get_daily call
        mock_ts_instance = mock_ts.return_value
        mock_ts_instance.get_daily.side_effect = Exception("API Error")

        symbol = 'AAPL'
        start_date = '2020-01-01'
        end_date = '2020-01-02'
        response = data_fetcher.get_stock_data(symbol, start_date, end_date)

        self.assertTrue(response.empty)

    @patch('data.data_fetcher.requests.Session')
    def test_get_active_stocks_unsuccessful(self, mock_session):
        # Simulate a failed response from the requests call
        mock_session.return_value.__enter__.return_value.get.side_effect = Exception("Network Error")

        with self.assertRaises(Exception) as context:
            data_fetcher.get_active_stocks()

        self.assertIn("Network Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()
