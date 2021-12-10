__author__ = 'akashjeez'

# Install Below Python Modules in Command Line / Terminal.
# >>> pip install --upgrade streamlit requests numpy pandas

import os, re, json, math, time, random
import requests, pandas, numpy
from PIL import Image
import streamlit as st
from datetime import datetime, timedelta

# #--------------------------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config(page_title = 'Py😎Streamlit', page_icon = '🔥', layout = 'wide', initial_sidebar_state = 'auto')

st.title(body = 'Py😎Streamlit')

#--------------------------------------------------------------------------------------------------------------------------------------#

def Execute_Main() -> None:
	try:
		st.sidebar.info(body = 'Developed by AkashJeez!')
		st.write('TESTING!!')
        #st.experimental_show( dataframe )

	except Exception as ex:
		print(f' Error : { ex } ')

#--------------------------------------------------------------------------------------------------------------------------------------#

## Execute the Main Code!

if __name__ == '__main__':
	Execute_Main()

#--------------------------------------------------------------------------------------------------------------------------------------#