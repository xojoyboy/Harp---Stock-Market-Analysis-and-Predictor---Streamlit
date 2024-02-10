from fetching.data_fetcher import get_stock_data

class Stock:
    """
    Class to represent a stock. It contains the stock symbol and the stock data.
    It also contains methods to calculate technical indicators.
    technical indicators are calculated using the stock data and added to the data.
    they incldue:
    - Simple Moving Average (SMA)
    - Exponential Moving Average (EMA)
    - Relative Strength Index (RSI)
    - Moving Average Convergence Divergence (MACD)
    - Bollinger Bands
    
    Parameters: symbol (string) - the stock symbol
    """
    def __init__(self, symbol):
        if not symbol or not isinstance(symbol, str):
            raise ValueError("Symbol symbol must a non-empty string")
        self.symbol = symbol
        self.data = None
    
    def initialize_data(self, start_date, end_date):
        """
        Initialize the stock data by fetching it from the API using the get_stock_data() 
        function given the start and end dates.
        """
        if not start_date or not end_date:
            raise ValueError("Start and end dates must be provided")
        self.data = get_stock_data(self.symbol, start_date, end_date)
        if self.data.empty:
            raise ValueError(f"No data found for {'self.symbol'} in given date range")

    def _get_price_column(self):
        """
        Helper method to get the correct price column.
        The price column is assumed to be either 'Close' or '4. close'
        and it is used to calculate technical indicators.
        This is important because the API returns the price column with different names
        and is a primary key for calculating technical indicators.
        """
        if 'Close' in self.data.columns:
            return 'Close'
        elif '4. close' in self.data.columns:
            return '4. close'
        else:
            raise ValueError("Expected price column not found in data")

    def calculate_sma(self, window):
        """
        Calculate Simple Moving Average (SMA).
        SMA is calculated by taking the average of the stock price over the given window.
        You can read more about SMA here: https://www.investopedia.com/terms/s/sma.asp
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be positive integer")
        price_col = self._get_price_column()
        self.data[f'SMA_{window}'] = self.data[price_col].rolling(window=window).mean()

    def calculate_ema(self, window):
        """
        Calculate Exponential Moving Average (EMA).
        EMA = Price(t) * k + EMA(y) * (1 - k)
        t = today, y = yesterday, N = number of days in EMA, k = 2/(N+1)
        you can read more about EMA here: https://www.investopedia.com/terms/e/ema.asp
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be positive integer")
        price_col = self._get_price_column()
        self.data[f'EMA_{window}'] = self.data[price_col].ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, window):
        """
        Calculate Relative Strength Index (RSI).
        RSI is calculated using the price change over the given window. It is a momentum indicator.
        You can read more about RSI here: https://www.investopedia.com/terms/r/rsi.asp
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be positive integer")
        price_col = self._get_price_column()
        delta = self.data[price_col].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        avg_gain = up.ewm(com=window-1, adjust=False).mean()
        avg_loss = down.ewm(com=window-1, adjust=False).mean()
        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

    def calculate_mov_avg_convergence_divergence(self, short_window, long_window):
        """
        Calculate Moving Average Convergence Divergence (MACD).
        MACD is calculated by subtracting the long term EMA from the short term EMA.
        Long term EMA is calculated over a longer window than the short term EMA.
        you can read more about MACD here: https://www.investopedia.com/terms/m/macd.asp
        """
        if not isinstance(short_window, int) or short_window <= 0:
            raise ValueError("Short window must be positive integer")
        price_col = self._get_price_column()
        self.calculate_ema(short_window)
        self.calculate_ema(long_window)
        self.data['MACD'] = self.data[f'EMA_{short_window}'] - self.data[f'EMA_{long_window}']
        self.data['Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
        self.data['MACD Histogram'] = self.data['MACD'] - self.data['Signal']

    def calculate_bollinger_bands(self, window):
        """
        Calculate Bollinger Bands.
        Bollinger Bands are calculated using the simple moving average (SMA) and standard deviation.
        You can read more about Bollinger Bands here: https://www.investopedia.com/terms/b/bollingerbands.asp
        """
        if not isinstance(window, int) or window <= 0:
            raise ValueError("Window must be positive integer")
        price_col = self._get_price_column()
        sma = self.data[price_col].rolling(window=window).mean()
        std_dev = self.data[price_col].rolling(window=window).std()
        self.data['Upper Band'] = sma + (std_dev * 2)
        self.data['Lower Band'] = sma - (std_dev * 2)
