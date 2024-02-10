Overview

HARP is an innovative tool designed for exploring stock market data, suitable for users ranging from beginners to 
seasoned investors. It transforms complex financial data into accessible, interactive insights, enabling analysis, comparison of stocks, 
understanding of market trends, and facilitation of informed investment decisions.

A. Environment Setup
- Library Dependencies:
   - alpha_vantage: For fetching financial data from Alpha Vantage API.
   - streamlit: To create the web application interface.
   - pandas: For data manipulation and analysis.
   - plotly: For interactive data visualizations.
   - scikit-learn: For implementing predictive models.
   - numpy

B. Installation and Execute Steps:
1.	Install required Python libraries: pip install alpha_vantage streamlit pandas plotly scikit-learn.
2.	Obtain an API key from Alpha Vantage and set it as an environment variable or in the configuration file.
3.	Put the key in the data_fetcher.py
4.	Run the Streamlit application: streamlit run app.py in cmd or terminal.
      - Remember to path to main directory if it cannot find app.py
  
Data Source and Integration
Central to HARP is the Alpha Vantage API, a key source for exhaustive and accurate financial datasets. This API provides current and historical stock data, vital for the application's core functionalities.
- Alpha Vantage API:
   - 	URL: Alpha Vantage Official Site: https://www.alphavantage.co/
   - 	Documentation: API Documentation: https://www.alphavantage.co/documentation/
   - 	Key Endpoints:
      - /query with TIME_SERIES_DAILY: Fetches daily stock prices (open, high, low, close, volume).
      - /query with LISTING_STATUS: Retrieves a list of active or delisted US stocks and ETFs.
  
Core Features
1.	Trend Visualization Page: Utilizes TIME_SERIES_DAILY for fetching daily stock data. Presents interactive charts for stock selection and time frame analysis, showcasing stock performance over time.
2.	Market Indicator Analysis Page: Leverages technical indicators (moving averages, RSI) calculated from daily stock data. Features interactive charts for indicators and stock price graphs.
3.	Stock Comparison Page: Enables comparison of multiple stocks using LISTING_STATUS data. Provides comparative charts for performance analysis.
4.	Stock Prediction Page: Utilizes the StockPredictor class's predictive analysis, forecasting future stock prices using linear regression.

Data Classes and Structures
- Stock Class: Manages individual stock data and technical indicator calculations. Method descriptions:
   - __init__(symbol): Initializes with stock symbol.
   - initialize_data(start_date, end_date): Fetches and stores stock data.
   - calculate_sma(window): Calculates Simple Moving Average.
   - calculate_ema(window): Computes Exponential Moving Average.
   - calculate_rsi(window): Determines Relative Strength Index.
   - calculate_bollinger_bands(window): Generates Bollinger Bands.
     
- StockPredictor Class: Facilitates predictive analysis using linear regression. Method descriptions:
   - __init__(stock_symbol): Initializes with stock symbol.
   - fetch_and_prepare_data(start_date, end_date): Prepares data for model training.
   - train_model(): Trains linear regression model.
   - predict_future_price(future_date): Predicts future stock price.
     
Data Processing and Handling
- Data Fetching (data_fetcher.py): Manages API calls and error handling, ensuring clean data delivery. Functions:
   - get_stock_data(symbol, start_date, end_date): Fetches and filters historical stock data.
   - get_active_stocks(): Retrieves current list of active stocks.

  

