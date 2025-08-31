import investpy
import streamlit as st

try:
    dataset = investpy.get_stock_historical_data(
        stock = 'AAPL',
        country = 'United States',
        from_date = '01/01/2025',
        to_date = '01/09/2025'
    )
    st.dataframe(data = dataset)
except Exception as ex:
    st.error(f'Error: {ex}')