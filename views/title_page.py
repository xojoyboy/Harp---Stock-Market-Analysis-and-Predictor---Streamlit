import streamlit as st

def show():
    """
    Home page for the app. It displays the title page of the app and a brief description of the app.
    """
    st.title('HARP')
    st.write('''
        Welcome to the HARP: your go-to instrument for stock analysis. This app provides insights into stock market trends, comparisons, and more.
        Use the sidebar to navigate through the app and explore different features.
    ''')
    