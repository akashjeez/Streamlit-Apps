__author__ = 'akashjeez'

import os, sys, re, time, math, json, pandas, numpy
import cv2, requests, random, string, base64
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image, ImageColor, ImageDraw, ImageEnhance
from io import BytesIO, TextIOWrapper

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config(page_title = 'PY☢P€NCV', page_icon = '🔥', layout = 'wide', initial_sidebar_state = 'auto')

st.title(body = 'PY☢P€NCV')

#----------------------------------------------------------------------------------------------------------------------#

CATEGORIES: dict = {
	'Catalog': None,
	'Image Analysis': ('Read Image', 'Face Detection', 'Eye Detection', 'Smile Detection', 'Pencil Sketch', 
		'Text to Image'),
	'Video Analysis': (),
}

## OpenCV - 3 Color Channels
BLUE, GREEN, RED = (255, 0, 0), (0, 255, 0), (0, 0, 255)

COLOR_MAPS: dict = { name : code for name, code in ImageColor.colormap.items() }

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


@st.cache
def Detect_Faces(input_image):
	input_image = numpy.array( object = input_image.convert('RGB') )
	new_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2BGRA )
	gray_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2GRAY )
	## Detect Faces
	faces = face_cascade.detectMultiScale(image = gray_image, scaleFactor = 1.1, minNeighbors = 4)
	## Draw Rectangle Around the Faces
	for (x, y, w, h) in faces:
		cv2.rectangle(img = new_image, color = BLUE, thickness = 2,
			pt1 = (x, y), pt2 = (x + w, y + h) )
	return new_image, faces


@st.cache
def Detect_Eyes(input_image):
	input_image = numpy.array( object = input_image.convert('RGB') )
	new_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2BGRA )
	gray_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2GRAY )
	## Detect Eyes
	eyes = eye_cascade.detectMultiScale(image = gray_image, scaleFactor = 1.3, minNeighbors = 5)
	## Draw Rectangle Around the Eyes
	for (ex, ey, ew, eh) in eyes:
		cv2.rectangle(img = new_image, color = GREEN, thickness = 2,
			pt1 = (ex, ey), pt2 = (ex + ew, ey + eh) )
	return new_image, eyes


@st.cache
def Detect_Smiles(input_image):
	input_image = numpy.array( object = input_image.convert('RGB') )
	new_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2BGRA )
	gray_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2GRAY )
	## Detect Eyes
	smiles = smile_cascade.detectMultiScale(image = gray_image, scaleFactor = 1.1, minNeighbors = 4)
	## Draw Rectangle Around the Smiles
	for (x, y, w, h) in smiles:
		cv2.rectangle(img = new_image, color = BLUE, thickness = 2,
			pt1 = (x, y), pt2 = (x + w, y + h) )
	return new_image, smiles


@st.cache
def Pencil_Sketch(input_image):
	input_image = numpy.array( object = input_image.convert('RGB') )
	gray_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2GRAY )
	image_invert = cv2.bitwise_not( src = gray_image )
	image_smoothing = cv2.GaussianBlur(src = image_invert, 
		ksize = (21, 21), sigmaX = 0, sigmaY = 0)
	final_image = cv2.divide( src1 = gray_image, src2 = 255 - image_smoothing, scale = 256 )
	return final_image	


#----------------------------------------------------------------------------------------------------------------------#

def EXECUTE_MAIN() -> None:
	st.sidebar.subheader(body = 'About Me')
	st.sidebar.info(body = '''
		Developed by AkashJeez :) \n
		Feel Free to Reach Out to Me Via \n
		[ << Website >>   ] ( https://akashjeez.herokuapp.com/ ) \n
		[ << Blogspot >>  ] ( https://akashjeez.blogspot.com/ ) \n
		[ << Instagram >> ] ( https://instagram.com/akashjeez/ ) \n
		[ << Twitter >>   ] ( https://twitter.com/akashjeez/ ) \n
		[ << GitHub >>    ] ( https://github.com/akashjeez/ ) \n
		[ << Dev.to >>    ] ( https://dev.to/akashjeez/ ) \n
		[ << LinkedIn >>  ] ( https://linkedin.com/in/akash-ponnurangam-408363125/ ) \n
	''')

	col_1, col_2 = st.beta_columns((2, 2))
	CATEGORY: str = col_1.selectbox(label = 'Choose Category', options = list(CATEGORIES.keys()) )
	st.write('*' * 50)

	if CATEGORY == 'Catalog':
		st.write('** Catalog ** Page Shows the List of Micro Apps Based on Category & Sub-Category in this Web Application.')
		st.table( data = [{'CATEGORY': key, 'SUB_CATEGORY': data} for key, value in CATEGORIES.items() \
			if value is not None for data in value] )

	elif CATEGORY == 'Image Analysis':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Read Image':
			try:
				st.write('** OpenCV Read Image **')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					our_image = Image.open( fp = image_file, mode = 'r' )
					new_image = cv2.cvtColor( src = numpy.array( object = our_image.convert('RGB') ), 
						code = cv2.COLOR_BGR2BGRA )
					st.image(image = our_image, caption = 'Original Image from PIL', use_column_width = True)
					st.image(image = new_image, caption = 'Original Image from OpenCV', use_column_width = True)
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'Face Detection':
			try:
				st.write('** OpenCV Face Detection **')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_faces = Detect_Faces( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Face Detection', use_column_width = True)
					st.success(f'Found { len(result_faces) } Faces!')
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'Eye Detection':
			try:
				st.write('** OpenCV Eye Detection **')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_eyes = Detect_Eyes( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Eye Detection', use_column_width = True)
					st.success(f'Found { len(result_eyes) } Eyes!')
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'Smile Detection':
			try:
				st.write('** OpenCV Smile Detection **')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_smiles = Detect_Smiles( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Smile Detection', use_column_width = True)
					st.success(f'Found { len(result_smiles) } Smiles!')
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'Pencil Sketch':
			try:
				st.write('** OpenCV Pencil Sketch **')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image = Pencil_Sketch( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Pencil Sketch', use_column_width = True)
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'Text to Image':
			try:
				st.write('** Text to Image Conversion **')
				col_1, col_2, col_3 = st.beta_columns((3, 2, 2))
				Input_Text: str = col_1.text_area(label = 'Enter Your Text', height = 4)
				Input_BG_Color: str = col_2.selectbox(label = 'Choose Background Color', options = list(set(COLOR_MAPS.keys())) )
				Input_Size: tuple = col_3.selectbox(label = 'Choose Image Resolution Size', options = [(i, i) for i in range(400, 1600, 100)] )
				if Input_Text is not None and Input_BG_Color is not None and Input_Size is not None:
					output = BytesIO()
					img = Image.new(mode = 'RGB', size = Input_Size, color = Input_BG_Color)
					draw_text = ImageDraw.Draw(im = img)
					draw_text.text((15, 15), Input_Text, fill = (255, 255, 0))
					img.save(fp = output, format = 'png')
					st.text('Right Click on Image and Save It On Your PC / Laptop / Smartphone!')
					st.image(image = output.getvalue(), use_column_width = False)
			except Exception as ex:
				st.write(f'** Error : ** { ex } ')


	elif CATEGORY == 'Video Analysis':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )
		st.write('** Coming Soon! **')


#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#