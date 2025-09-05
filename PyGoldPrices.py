import os, sys, warnings
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

warnings.filterwarnings(action = 'ignore')

#################

st.set_page_config(page_title = 'Gold Price Analysis', page_icon = '🪙', layout = 'wide')

try:
    st.header('Gold Price Analysis')
    
    #Data_File: str = 'C:/PythonExcels/Gold-Price-Historical.csv'
    Data_File: str = 'https://raw.githubusercontent.com/akashjeez/Streamlit-Apps/main/Gold-Price-Historical.csv'
    df = pd.read_csv(filepath_or_buffer = Data_File)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(arg = df['Date'], format = '%Y-%m-%d', errors = 'coerce')

    original_df = df.copy()

    c_1, c_2 = st.columns([2, 2])
    Start_Date = c_1.date_input(label = 'Select Start Date', 
        value = datetime.now() - timedelta(days = 30),
        min_value = df['Date'].min(), max_value = df['Date'].max() 
    )
    Predict_Days: int = c_2.slider(label = 'Select Days to Predict', min_value = 1, max_value = 30, value = 7, step = 1)

    df = df[ (df['Date'] >= pd.to_datetime( Start_Date )) ]

    if len( df ) > 0:
        c_1, c_2 = st.columns([2, 3])
        df = df.sort_values('Date', ascending = False).reset_index(drop = True)
        c_1.dataframe(data = df, use_container_width = True)
        c_2.line_chart(data = df, x = 'Date', y = ['24K_Gold', '22K_Gold'], width = 0, height = 500)

        c_1.subheader(body = f'Predicted Gold Price for Next {Predict_Days} Days')
        original_df = original_df.sort_values('Date').reset_index(drop = True)
        original_df['24K_prev'] = original_df['24K_Gold'].shift(1)
        original_df['22K_prev'] = original_df['22K_Gold'].shift(1)
        original_df = original_df.dropna()
        X = original_df[['24K_prev', '22K_prev']]
        y_24k = original_df['24K_Gold']
        y_22k = original_df['22K_Gold']
        model_24k = LinearRegression().fit(X, y_24k)
        model_22k = LinearRegression().fit(X, y_22k)
        model_22k_score: float = round(model_22k.score(X, y_22k) * 100, 2)
        model_24k_score: float = round(model_24k.score(X, y_24k) * 100, 2)
        c_1.write(f' Model Score for 24 K = { model_24k_score } % || 22K : { model_22k_score } %')
        predictions: int = []
        last_24k = original_df['24K_Gold'].iloc[-1]
        last_22k = original_df['22K_Gold'].iloc[-1]
        last_date = original_df['Date'].max()
        for i in range(int(Predict_Days)):
            pred_24k = model_24k.predict([[last_24k, last_22k]])[0]
            pred_22k = model_22k.predict([[last_24k, last_22k]])[0]
            pred_date = last_date + timedelta(days = i + 1)
            predictions.append({'Date': pred_date, '24K_Gold': int(pred_24k), '22K_Gold': int(pred_22k) })
            last_24k = pred_24k
            last_22k = pred_22k
        pred_df = pd.DataFrame(data = predictions)
        c_1.dataframe(data = pred_df)
        c_2.line_chart(data = pred_df, x = 'Date', y = ['24K_Gold', '22K_Gold'], width = 0, height = 500)
    else:
        st.warning(body = f' No Data Found for the Selected Date Range: { Start_Date } ')

except Exception as ex:
    st.error(body = f'Error : { ex }')
