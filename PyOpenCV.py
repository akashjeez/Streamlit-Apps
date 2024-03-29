__author__ = 'akashjeez'

import os, sys, re, csv, base64
import pandas, numpy, cv2, qrcode
#from pyzbar import pyzbar
import streamlit as st
from datetime import datetime, timedelta
from PIL import Image, ImageColor, ImageDraw, ImageEnhance
from io import BytesIO, StringIO, TextIOWrapper

#--------------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config(page_title = 'PY☢P€NCV', page_icon = '🔥', layout = 'wide', initial_sidebar_state = 'auto')

st.title(body = 'PY☢P€NCV')

#--------------------------------------------------------------------------------------------------------------------------#

CATEGORIES: dict = {
	'Catalog': None,
	'Image Analysis': ('Read Image', 'Face Detection', 'Eye Detection', 'Smile Detection', 'Pencil Sketch', 
		'QR Code', 'Text to Image', ),
	'Video Analysis': (),
}

## OpenCV - 3 Color Channels
BLUE, GREEN, RED = (255, 0, 0), (0, 255, 0), (0, 0, 255)

COLOR_MAPS: dict = { name : code for name, code in ImageColor.colormap.items() }

if os.path.isdir('OpenCV'):
	face_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_eye.xml')
	smile_cascade = cv2.CascadeClassifier('OpenCV/haarcascade_smile.xml')

#--------------------------------------------------------------------------------------------------------------------------#

def Data_Downloader(df: pandas.DataFrame) -> str:
    ## Excel Worksheet Limitation = 1,048,576 Rows X 16,384 Columns
    if 0 < len( df ) < 1048576 and 0 < len( df.columns ) < 16384:
        output = BytesIO()
        writer = pandas.ExcelWriter(path = output, engine = 'xlsxwriter')
        df.to_excel(excel_writer = writer, sheet_name = 'Data', index = False )
        writer.close()
        processed_data: bytes = output.getvalue()
        b64: bytes = base64.b64encode( processed_data )
        return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"
    else:
        output = StringIO()
        csv.writer( output ).writerows( [list(df.columns)] + df.values.tolist() )
        processed_data: bytes = output.getvalue().encode()
        b64: bytes = base64.b64encode( processed_data )
        return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.csv'> Download CSV </a>"


@st.cache_data
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


@st.cache_data
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


@st.cache_data
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


@st.cache_data
def Pencil_Sketch(input_image):
	input_image = numpy.array( object = input_image.convert('RGB') )
	gray_image = cv2.cvtColor( src = input_image, code = cv2.COLOR_BGR2GRAY )
	image_invert = cv2.bitwise_not( src = gray_image )
	image_smoothing = cv2.GaussianBlur(src = image_invert, 
		ksize = (21, 21), sigmaX = 0, sigmaY = 0)
	final_image = cv2.divide( src1 = gray_image, src2 = 255 - image_smoothing, scale = 256 )
	return final_image	


#--------------------------------------------------------------------------------------------------------------------------#

def Execute_Main() -> None:

	with st.sidebar:
		with st.expander(label = 'About Me', expanded = False):
			st.info(body = '''
				Developed by AkashJeez :) \n
				Feel Free to Reach Out to Me Via \n
				[<< LinkTree >>](https://linktr.ee/akashjeez) \n
				[<< GitHub >>](https://github.com/akashjeez/) \n
			''')

	col_1, col_2 = st.columns((2, 2))
	CATEGORY: str = col_1.selectbox(label = 'Choose Category', options = list(CATEGORIES.keys()) )
	st.write('*' * 50)

	if CATEGORY == 'Catalog':
		st.write('**Catalog** Page Shows the List of Micro Apps Based on Category & Sub-Category in this Web Application.')
		st.table( data = [ {'CATEGORY': key, 'SUB_CATEGORY': data} for key, value in CATEGORIES.items() \
			if value is not None for data in value ] )

	elif CATEGORY == 'Image Analysis':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Read Image':
			try:
				st.write('**OpenCV Read Image**')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					our_image = Image.open( fp = image_file, mode = 'r' )
					new_image = cv2.cvtColor( src = numpy.array( object = our_image.convert('RGB') ), 
						code = cv2.COLOR_BGR2BGRA )
					st.image(image = our_image, caption = 'Original Image from PIL', use_column_width = True)
					st.image(image = new_image, caption = 'Original Image from OpenCV', use_column_width = True)
			except Exception as ex:
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'Face Detection':
			try:
				st.write('**OpenCV Face Detection**')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_faces = Detect_Faces( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Face Detection', use_column_width = True)
					st.success(f'Found { len(result_faces) } Faces!')
			except Exception as ex:
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'Eye Detection':
			try:
				st.write('**OpenCV Eye Detection**')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_eyes = Detect_Eyes( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Eye Detection', use_column_width = True)
					st.success(f'Found { len(result_eyes) } Eyes!')
			except Exception as ex:
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'Smile Detection':
			try:
				st.write('**OpenCV Smile Detection**')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image, result_smiles = Detect_Smiles( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Smile Detection', use_column_width = True)
					st.success(f'Found { len(result_smiles) } Smiles!')
			except Exception as ex:
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'Pencil Sketch':
			try:
				st.write('**OpenCV Pencil Sketch**')
				image_file = st.file_uploader(label = 'Choose an Image', accept_multiple_files = False, 
					type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
				if image_file is not None:
					input_image = Image.open( fp = image_file, mode = 'r' )
					result_image = Pencil_Sketch( input_image = input_image )
					st.image(image = input_image, caption = 'Original Image', use_column_width = True)
					st.image(image = result_image, caption = 'Pencil Sketch', use_column_width = True)
			except Exception as ex:
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'Text to Image':
			try:
				st.write('**Text to Image Conversion**')
				col_1, col_2, col_3 = st.columns((3, 2, 2))
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
				st.write(f'**Error :** { ex } ')

		elif SUB_CATEGORY == 'QR Code':
			try:
				st.write('**QR Code Generator and Decoder**')
				col_1, col_2 = st.columns((2, 2))
				type: tuple = col_1.selectbox(label = 'Generator / Decoder', options = ('Generator', 'Decoder') )
				if type == 'Generator':
					input_text: str = col_2.text_area(label = 'Enter Your Text', height = 4)
					if input_text is not None:
						output = BytesIO()
						img = qrcode.make( data = input_text )
						img.save( output )
						st.image( image = output.getvalue(), width = 300, use_column_width = False )
				elif type == 'Decoder':
					st.warning(body = 'Coming Soon..')
					# image_file = col_2.file_uploader(label = 'Chooose Bar / QR Code Image', accept_multiple_files = False, 
					# 	type = ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP', 'TIFF'] )
					# if image_file is not None:
					# 	input_image = Image.open( fp = image_file, mode = 'r' )
					# 	st.image(image = input_image, caption = 'Original Image', width = 100, use_column_width = True)
					# 	st.text('Extracted Text Data from Image..')
					# 	for barcode in pyzbar.decode( input_image ):
					# 		st.success( barcode.data.decode('utf-8').strip() )
			except Exception as ex:
				st.write(f'**Error :** { ex } ')


	elif CATEGORY == 'Video Analysis':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )
		st.write('**Coming Soon!**')


#--------------------------------------------------------------------------------------------------------------------------#

## Run the Main Code!

if __name__ == '__main__':
	Execute_Main()

#--------------------------------------------------------------------------------------------------------------------------#