'''
# Historical Data: Gold Price USD = https://in.investing.com/commodities/gold-historical-data
# Historical Data: USD INR Currency = https://in.investing.com/currencies/usd-inr-historical-data
'''

import os, sys, json
import warnings, joblib
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

warnings.filterwarnings(action = 'ignore')

#################

st.set_page_config(page_title = 'Gold Price Analysis', page_icon = '🪙', layout = 'wide')

try:
    st.header('Gold Price Analysis')
    #os.chdir(path = 'C:/PythonExcels/Gold-Price-Prediction')
    Data_File = 'gold-price-data.csv'
    #Gold_Price_USD_Model_File = 'Models/Gold_Price_USD_Model.pkl'
    #USD_INR_Model_file = 'Models/USD_INR_Model.pkl'

    if not os.path.exists(path = Data_File):
        st.error(body = f'Source Flat File Not Found: { Data_File }')
        sys.exit(1)

    df = pd.read_csv(filepath_or_buffer = Data_File)
    df['Date'] = pd.to_datetime(df['Date'])
    #df['Date'] = pd.to_datetime(df['Date'],  format = '%d-%m-%y').dt.strftime('%Y-%m-%d')
    df['Actual_Gold_Price_USD'] = df['Actual_Gold_Price_USD'].round(2)
    df['Actual_USD_INR'] = df['Actual_USD_INR'].round(2)
    # Calculate Gold_Price_INR and Gold_Price_INR_per_Gram
    df['Actual_Gold_Price_INR'] = (df['Actual_Gold_Price_USD'] * df['Actual_USD_INR']).round(2)
    df['Actual_Gold_Price_INR_per_Gram'] = (df['Actual_Gold_Price_INR'] / 31.1035).round(2)
    st.dataframe(data = df, use_container_width = True)

    ## Sort by date ascending
    df = df.sort_values('Date').reset_index(drop = True)

    ## Create lag features (previous day's values)
    df['Gold_Price_USD_prev'] = df['Actual_Gold_Price_USD'].shift(1)
    df['USD_INR_prev'] = df['Actual_USD_INR'].shift(1)
    df = df.dropna().reset_index(drop = True)

    ## Features and targets
    X = df[['Gold_Price_USD_prev', 'USD_INR_prev']]
    y_usd = df['Actual_Gold_Price_USD']
    y_inr = df['Actual_USD_INR']

    ## Split into train/test for scoring
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_usd_train, y_usd_test = y_usd.iloc[:split_idx], y_usd.iloc[split_idx:]
    y_inr_train, y_inr_test = y_inr.iloc[:split_idx], y_inr.iloc[split_idx:]

    ## Train new models
    model_usd = LinearRegression().fit(X_train, y_usd_train)
    model_inr = LinearRegression().fit(X_train, y_inr_train)

    ##Evaluate new models
    # usd_score = r2_score(y_usd_test, model_usd.predict(X_test))
    # inr_score = r2_score(y_inr_test, model_inr.predict(X_test))

    # st.write(f'R2 Score for Gold Price USD Model: {usd_score:.2f}')
    # st.write(f'R2 Score for USD to INR Model: {inr_score:.2f}')

    ## Start with the latest known values
    last_usd = df.iloc[-1]['Actual_Gold_Price_USD']
    last_inr = df.iloc[-1]['Actual_USD_INR']
    last_date = pd.to_datetime(df['Date'].max())

    features = np.array([[last_usd, last_inr]])
    pred_usd: float = (model_usd.predict(features)[0]).round(2)
    pred_inr: float = (model_inr.predict(features)[0]).round(2)
    pred_gold_inr: float = (pred_usd * pred_inr).round(2)
    pred_gold_inr_per_gram: float = (pred_gold_inr / 31.1035).round(2)

    st.write('Predictions for tomorrow:')
    st.write(f'Date = { last_date + timedelta(days = 1):%Y-%m-%d }')
    st.write(f'Predicted Gold Price in USD = { pred_usd }')
    st.write(f'Predicted USD to INR = { pred_inr }')
    st.write(f'Predicted Gold Price in INR = { pred_gold_inr }')
    st.write(f'Predicted Gold Price in INR per Gram = { pred_gold_inr_per_gram }')
    
except Exception as ex:
    st.error(body = f'Error : { ex }')
