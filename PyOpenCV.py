__author__ = 'akashjeez'

import os, sys, re, time, math, json, pandas, numpy
import cv2, requests, random, string, base64
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image, ImageEnhance
from io import BytesIO, TextIOWrapper

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('PY☢ṕ€NCV')

#----------------------------------------------------------------------------------------------------------------------#

CATEGORIES_LIST: list = ['Read Image']
CATEGORIES_LIST.sort()

## OpenCV - 3 Color Channels
BLUE, GREEN, RED = (255, 0, 0), (0, 255, 0), (0, 0, 255)

if os.path.isdir('OpenCV'):
	face_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_eye.xml')
	smile_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_smile.xml')

#----------------------------------------------------------------------------------------------------------------------#

def Excel_Downloader(df: pandas.DataFrame) -> str:
	output = BytesIO()
	writer = pandas.ExcelWriter(path = output, engine = 'xlsxwriter')
	df.to_excel(excel_writer = writer, sheet_name = 'Data')
	writer.save()
	processed_data = output.getvalue()
	b64 = base64.b64encode(processed_data)
	return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"

#----------------------------------------------------------------------------------------------------------------------#

def EXECUTE_MAIN() -> None:
	st.sidebar.subheader('Contribute')
	st.sidebar.info('''
		This is an Open Source Project and You are Very Welcome to Contribute 
		Your Awesome Comments, Questions, Resources and Apps as
		[Issues] ( https://github.com/akashjeez/Streamlit-Apps/issues )
		of or [Pull Requests] ( https://github.com/akashjeez/Streamlit-Apps/pulls )
		to the [Source Code] ( https://github.com/akashjeez/Streamlit-Apps ).
	''')

	st.sidebar.subheader('About Me')
	st.sidebar.info('''
		Hi there, I am AkashJeez, Love Coding and Racing :) \
		Feel Free to Reach Out to Me Via \n
		[ << Website >> ] ( https://akashjeez.herokuapp.com/ ) \n
		[ << Blogspot >> ] ( https://akashjeez.blogspot.com/ ) \n
		[ << Instagram >> ] ( https://instagram.com/akashjeez/ ) \n
		[ << Twitter >> ] ( https://twitter.com/akashjeez/ ) \n
		[ << Github >> ] ( https://github.com/akashjeez/ ) \n
		[ << Tubmlr >> ] ( https://akashjeez.tumblr.com/ ) \n
		[ << LinkedIn >> ] ( https://linkedin.com/in/akash-ponnurangam-408363125/ ) \n
	''')

	CATEGORY = st.selectbox(label = 'Choose Micro App', options = CATEGORIES_LIST)

	st.write('*' * 100)

	if CATEGORY == 'Read Image':
		try:
			st.write('** OpenCV Read Image **')
			image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
				type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
			if image_file is not None:
				our_image = Image.open( fp = image_file, mode = 'r' )
				new_image = cv2.cvtColor( src = numpy.array( our_image.convert('RGB') ), 
					code = cv2.COLOR_BGR2BGRA )
				st.image(image = our_image, caption = 'Original Image', use_column_width = True)
				st.image(image = new_image, caption = 'OpenCV Image', use_column_width = True)
		except Exception as ex:
			st.write(f'** Error : ** { ex } ')


#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#