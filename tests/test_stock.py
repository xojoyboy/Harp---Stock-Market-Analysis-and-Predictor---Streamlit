"""
Very hard to test the stock class due to its dependency on the AlphaVantage API. 
The data returned from the API is not static and changes over time.
The results are also dependent on the window size used to calculate the technical indicators.
"""

import sys
sys.path.append('C:\\Users\\slaye\\OneDrive\\Desktop\\NEU\\5001\\Final Project\\Harp')
import unittest
from unittest.mock import patch
from models.stock import Stock
import pandas as pd

def get_stock_data_mock(symbol, start_date, end_date):
    data = pd.DataFrame({
        '4. close': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
        '5. volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
    }, index=pd.date_range(start='2020-01-01', periods=10))
    return data

class TestStock(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('TEST')
        self.stock.data = get_stock_data_mock('TEST', '2020-01-01', '2020-01-10')

    def test_calculate_sma(self):
        self.stock.calculate_sma(3)
        expected_sma = [None, None, 110, 120, 130, 140, 150, 160, 170, 180]
        pd.testing.assert_series_equal(self.stock.data['SMA_3'], pd.Series(expected_sma, name='SMA_3', index=self.stock.data.index))

    def test_calculate_sma(self):
        self.stock.calculate_sma(3)
        expected_sma = [None, None, 110, 120, 130, 140, 150, 160, 170, 180]
        pd.testing.assert_series_equal(self.stock.data['SMA_3'], pd.Series(expected_sma, name='SMA_3', index=self.stock.data.index))

    def test_calculate_ema(self):
        self.stock.calculate_ema(2)
        expected_ema = [100.0, 106.66666666666666, 115.55555555555556, 125.18518518518519,
                        135.06172839506172, 145.02057613168725, 155.00685871056243,
                        165.00228623685413, 175.00076207895137, 185.00025402631712]
        pd.testing.assert_series_equal(self.stock.data['EMA_2'], pd.Series(expected_ema, name='EMA_2', index=self.stock.data.index))

    def test_calculate_rsi(self):
        self.stock.calculate_rsi(2)
        expected_rsi = [None, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        pd.testing.assert_series_equal(self.stock.data['RSI'], pd.Series(expected_rsi, name='RSI', index=self.stock.data.index))

    def test_calculate_mov_avg_convergence_divergence(self):
        self.stock.calculate_mov_avg_convergence_divergence(2, 5)
        expected_macd = [0.0, 3.3333333333333144, 6.666666666666657, 9.259259259259252,
                         11.111111111111086, 12.38683127572014, 13.251028806584344,
                         13.831732967535402, 14.220393232738871, 14.480008128842115]
        expected_signal = [0.0, 0.666666666666663, 1.8666666666666618, 3.34518518518518,
                           4.898370370370362, 6.396062551440318, 7.767055802469123,
                           8.97999123548238, 10.02807163493368, 10.918458933715367]
        pd.testing.assert_series_equal(self.stock.data['MACD'], pd.Series(expected_macd, name='MACD', index=self.stock.data.index))
        pd.testing.assert_series_equal(self.stock.data['Signal'], pd.Series(expected_signal, name='Signal', index=self.stock.data.index))

    def test_calculate_bollinger_bands(self):
        self.stock.calculate_bollinger_bands(2)
        expected_upper = [None, 119.14213562373095, 129.14213562373095, 139.14213562373095,
                          149.14213562373095, 159.14213562373095, 169.14213562373095,
                          179.14213562373095, 189.14213562373095, 199.14213562373095]
        expected_lower = [None, 90.85786437626905, 100.85786437626905, 110.85786437626905,
                          120.85786437626905, 130.85786437626905, 140.85786437626905,
                          150.85786437626905, 160.85786437626905, 170.85786437626905]
        pd.testing.assert_series_equal(self.stock.data['Upper Band'], pd.Series(expected_upper, name='Upper Band', index=self.stock.data.index))
        pd.testing.assert_series_equal(self.stock.data['Lower Band'], pd.Series(expected_lower, name='Lower Band', index=self.stock.data.index))

if __name__ == '__main__':
    unittest.main()
