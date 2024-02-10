import streamlit as st
from views import trend_visualization, market_indicator_analysis, stock_comparison, title_page, stock_prediction
from utility.get_stock_input import get_single_stock, get_multiple_stocks
from models.stock import Stock
from models.stock_predictor import StockPredictor
from datetime import date

def main():
    """
    Driver:
    
    It shows the sidebar and the main page based on the user's selection.
    The user can select the page from the sidebar.
    It uses get_single_stock() and get_multiple_stocks() functions to get the stock input from the user.
    It then initializes the Stock object and calls the appropriate function to show
    the page selected and passes the Stock object to the function.
    It also handles any errors that occur and displays them to the user.

    -Get the stock input from the user
    -Initialize the Stock object
    -Pass the Stock object to the appropriate view function selected by the user
    -Handle date input and date changes and pass the dates to the Stock object which 
    is then updated for the user in the views
    """
    try:
        logo_path = "Harp-Logo.png"
        st.sidebar.image(logo_path, use_column_width=True)

        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Go to", ["Home", "Trend Visualization", "Market Indicator Analysis", "Stock Comparison", "Stock Price Prediction"])

        if page == "Home":
            title_page.show()
        elif page in ["Trend Visualization", "Market Indicator Analysis"]:
            selected_stock = get_single_stock()

            if selected_stock:
                symbol = selected_stock['symbol']
                start_date = st.date_input("Start date", date.today().replace(year=date.today().year - 1))
                end_date = st.date_input("End date", date.today())

                stock = Stock(symbol)
                stock.initialize_data(start_date, end_date)

                if page == "Trend Visualization":
                    trend_visualization.show(stock)
                elif page == "Market Indicator Analysis":
                    market_indicator_analysis.show(stock)

        elif page == "Stock Comparison":
            selected_stocks = get_multiple_stocks()

            if selected_stocks:
                stocks = [Stock(stock['symbol']) for stock in selected_stocks]
                start_date = st.date_input("Start date", date.today().replace(year=date.today().year - 1))
                end_date = st.date_input("End date", date.today())

                for stock in stocks:
                    stock.initialize_data(start_date, end_date)

                stock_comparison.show(stocks)

        elif page == "Stock Price Prediction":
            selected_stock = get_single_stock()

            if selected_stock:
                symbol = selected_stock['symbol']
                future_date = st.date_input("Select Future Date", date.today())

                # Initialize the StockPredictor object with the selected stock symbol
                predictor = StockPredictor(symbol)

                stock_prediction.show_stock_prediction(predictor, future_date)
    except ValueError as e:
        st.error(e)
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
