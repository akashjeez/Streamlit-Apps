__author__ = 'akashjeez'

import os, sys, re, math, json, time
import random, string, base64, calendar
import requests, pafy, qrcode, hashlib, emojis
from datetime import datetime, timedelta
from io import BytesIO, TextIOWrapper
from fake_useragent import UserAgent
import pandas, numpy
import streamlit as st
import yfinance as yf
from GoogleNews import GoogleNews
from googletrans import Translator
from textblob import TextBlob, Word

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('Ak@$h😎J€€Z')

#----------------------------------------------------------------------------------------------------------------------#

CATEGORIES_LIST: list = ['Age Calculator', 'Python Tutorial', 'Google Translator', 'CoronaVirus Stats',
	'Stock Ticker', 'Urban Dictionary', 'Best Poetries', 'YouTube Downloader', 'Cloud Market Cost', 
	'AWS Cloud Cost', 'National Today', 'Google News', 'Other Tools', 'World Countries', 'Song Lyrics',
	'Text Analysis', 'Emojis Search', 'Microsoft Learn', 'Cricket IPL Stats', 'ICC Cricket World Cup Stats',
	'ICC Cricket Stats', 'Weather Report', 'Open Trivia', 'Proxy List', ]
CATEGORIES_LIST.sort()

LANGUAGES: dict = {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az', 
	'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 
	'Chinese (Traditional)': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 
	'Esperanto': 'eo', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 
	'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he', 
	'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 
	'Japanese': 'ja', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 
	'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 
	'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 
	'Norwegian': 'no', 'Nyanja (Chichewa)': 'ny', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese (Portugal, Brazil)': 'pt', 
	'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 
	'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 
	'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr',
	'Tagalog (Filipino)': 'tl', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 
	'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu' }

#----------------------------------------------------------------------------------------------------------------------#

def Excel_Downloader(df: pandas.DataFrame) -> str:
	output = BytesIO()
	writer = pandas.ExcelWriter(path = output, engine = 'xlsxwriter')
	df.to_excel(excel_writer = writer, sheet_name = 'Data')
	writer.save()
	processed_data = output.getvalue()
	b64 = base64.b64encode(processed_data)
	return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"


def Convert_Size(size_bytes: int) -> str:
	if size_bytes == 0:	return '0B'
	size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
	i = int( math.floor( math.log( size_bytes, 1024 ) ) )
	p = math.pow( 1024, i )
	s = round(size_bytes / p, 2)
	return f'{s} {size_name[i]}'


@st.cache
def YouTube_Downloader(video_id: str) -> dict:
	video = pafy.new( video_id )
	dataset = {
		'Title': video.title, 'Rating': video.rating, 'ViewCount': video.viewcount,
		'Author': video.username, 'Length': video.length, 'Duration': video.duration,
		'Category': video.category, 'Likes': video.likes, 'Dislikes': video.dislikes, 
	}
	video_dataset = [{
		'Resolution': stream.resolution, 'Extension': stream.extension.upper(),
		'FileSize': Convert_Size( stream.get_filesize() ),'DownloadLink': stream.url,
	} for stream in video.videostreams ]
	audio_dataset = [{
		'Extension': stream.extension.upper(), 'DownloadLink': stream.url,
		'FileSize': Convert_Size( stream.get_filesize() ), 
	} for stream in video.audiostreams ]
	dataset.update( { 'videos' : video_dataset, 'audios' : audio_dataset } )
	return dataset


@st.cache
def CoronaVirus_Stats() -> pandas.DataFrame:
	BASE_URL = 'https://covid.ourworldindata.org/data'
	covid_data = pandas.read_csv(f'{BASE_URL}/ecdc/full_data.csv')
	population_data = pandas.read_csv(f'{BASE_URL}/ecdc/locations.csv')
	dataset = pandas.merge(covid_data, population_data, on = 'location', how = 'left')
	dataset = dataset[ dataset.population_year == 2020.0 ]
	dataset.date = pandas.to_datetime( dataset.date, infer_datetime_format = True)
	dataset.drop(['countriesAndTerritories', 'population', 'population_year'], axis = 1, inplace = True)
	return dataset


@st.cache
def Cloud_Market_Cost(provider: str) -> dict:
	dataset, BASE_URL = [], 'https://banzaicloud.com/cloudinfo/api/v1/providers/{}/services/compute/regions'
	regions_data = requests.get( BASE_URL.format(provider), timeout = 300).json()
	for region in regions_data:
		response = requests.get( f"{BASE_URL.format(provider)}/{region['id']}/products", timeout = 300).json()
		if 'products' in response.keys():
			if len(response['products']) > 0:
				for product in response['products']:
					dataset.append({
						'Provider': provider.upper(),
						'Category': product.get('category', 'TBD'), 
						'Instance_type': product.get('type', 'TBD'),
						'CPU': int( product.get('cpusPerVm', 0) ),
						'Memory': round( float( product.get('memPerVm', 0) ), 1),
						'Cost_Per_Hour': round( float( product.get('onDemandPrice', 0) ), 3),
						'Region_ID': region.get('id', 'TBD'),
						'Region_Name': region.get('name', 'TBD'),
						'Network_Performance': product.get('ntwPerf', 'TBD'),
						'Network_Perf_Category': product.get('ntwPerfCategory', 'TBD')
					})
	return dataset

@st.cache
def Proxy_List(urls: list) -> pandas.DataFrame:
	headers = {'User-Agent': UserAgent().random}
	df_1 = pandas.read_html( requests.get(urls[0], headers = headers).text )[0]
	df_2 = pandas.read_html( requests.get(urls[1], headers = headers).text )[0]
	dataset = df_1.append(df_2, ignore_index = True)
	dataset.drop_duplicates(['IP Address'], inplace = True)
	dataset.dropna(inplace = True)
	return dataset

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
		Hi there, I am AkashJeez, I Love Coding and Racing :) \n
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

	if CATEGORY == 'Age Calculator':
		try:
			st.subheader('** Age Calculator **')
			input_date = st.date_input(label = 'Choose Date-of-Birth', value = (datetime.today() - timedelta(days = 18250)) )
			result: float = round( ( ( datetime.now().date() - input_date ).days / 365 ), 2)
			st.write(f'\n ** Your Age is { result } ** ')
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Python Tutorial':
		try:
			st.subheader('** Python Tutorial **')
			st.write('Python is a Powerful General Purpose Programming Language. It is used in Web Development, Data Science, \
				Creating Software Prototypes etc. Python has Simple Easy-To-Use Syntax and Excellent Language to Learn to Program for Beginners.')
			OnlineCompilerLink: str = 'https://console.python.org/python-dot-org-console/'
			st.markdown("<a href = 'https://twitter.com/ThePSF' class = 'twitter-timeline'> Follow @ThePSF </a> ", unsafe_allow_html = True)
			st.write('** Python Online Compiler - Interactive Shell **')
			st.markdown(f"<iframe src = '{OnlineCompilerLink}' width = 700 height = 300 frameborder = 0> </iframe>", unsafe_allow_html = True)
			st.write('*' * 100)
			st.write('** Online Python Learning **')
			st.markdown(f"<a href = 'https://w3schools.com/python/' target = '_blank'> << W3Schools >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://pythonprogramming.net/' target = '_blank'> << PythonProgramming.Net >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://programiz.com/python-programming' target = '_blank'> << ProgramiZ >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://datacamp.com/' target = '_blank'> << DataCamp >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://awesome-python.com/' target = '_blank'> << Awesome Python >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://realpython.com/' target = '_blank'> << Real Python >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://guide.freecodecamp.org/python/' target = '_blank'> << Free-Code-Camp >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://sololearn.com/Course/Python/' target = '_blank'> << SoloLearn >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://web.programminghub.io/' target = '_blank'> << Programming Hub >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://youtu.be/_uQrJ0TkZlc' target = '_blank'> << Youtube - Python Absolute for Beginners >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://data36.com/' target = '_blank'> << Python Data Science for Beginners >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://tutorialsteacher.com/python' target = '_blank'> << Tutorials Teacher >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://morioh.com' target = '_blank'> << Morioh >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://tutorialedge.net/course/python/' target = '_blank'> << Tutorials Edge >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://listendata.com/search/label/Python' target = '_blank'> << Listen Data >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://data-flair.training/blogs/python-tutorial/' target = '_blank'> << Data Flair >> </a>", unsafe_allow_html = True)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Google Translator':
		try:
			st.subheader('** Google Translator **')
			col_1, col_2 = st.beta_columns((2, 2))
			keyword: str = col_1.text_input(label = 'Enter Keyword', value = '')
			lang_name: list = col_2.selectbox(label = 'Choose Language', options = list(LANGUAGES.keys()) )
			if keyword and lang_name:
				translator = Translator(service_urls = ['translate.google.com'])
				result = translator.translate( keyword.strip(), dest = LANGUAGES[lang_name] )
				col_1.write(f'\n ** Input keyword : ** { keyword }')
				col_1.write(f' ** Input Language : ** { lang_name }')
				col_2.write(f' ** Result : ** { result.text }')
				col_2.write(f' ** Pronunciation : ** { result.pronunciation }')
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'CoronaVirus Stats':
		try:
			st.subheader('** CoronaVirus Stats **')
			## Load the DataSet with Streamlit Cache.
			filter_x: str = st.radio(label = 'Overview / Detailed Stats', options = ('Overiew Stats', 'Detailed Stats'))
			if filter_x == 'Overiew Stats':
				data_dump = CoronaVirus_Stats()
				col_1, col_2, col_3, col_4 = st.beta_columns((2, 2, 2, 2))
				categories: str = col_1.selectbox(label = 'Continents / Countries?', options = ['Continents', 'Countries'] )
				start_date: str = col_2.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 30)) )
				end_date: str = col_3.date_input(label = 'End Date', value = datetime.now() )
				start_date, end_date = str(start_date), str(end_date)
				if categories == 'Countries':
					locations: list = col_4.multiselect(label = 'Select Countries', default = ['India', 'United States'], 
				    	options = [country for country in data_dump.location.unique()] )
					st.write(f"** > Selected Countries are ** {', '.join( locations )} ")
					data_dump_1 = data_dump[ (data_dump.location.isin( locations )) ]
				else:
					continents: list = col_4.multiselect(label = 'Select Continents', default = ['Asia'], 
				    	options = [country for country in data_dump.continent.unique()] )
					st.write(f"** > Selected Continents are ** {', '.join( continents )} ")
					data_dump_1 = data_dump[ (data_dump.continent.isin( continents )) ]
				dataset = data_dump_1[ (data_dump_1.date >= start_date) & (data_dump_1.date <= end_date) ]
				st.write(f'** > Selected Date Range From ** { start_date } TO { end_date } ')
				st.write(f'** Stats = ** Cases : { int(dataset.new_cases.sum()) } | Deaths : { int(dataset.new_deaths.sum()) } ')
				## Download Excel File
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
				chart_data = dataset[['date', 'new_cases', 'new_deaths', 'total_cases', 'total_deaths']]
				chart_data.set_index('date', inplace = True)
				parameters = st.multiselect(label = 'Select Parameters', options = list(chart_data.columns), default = ['total_cases'], )
				st.line_chart( chart_data[parameters] if len(parameters) > 0 else chart_data['total_cases'] )
			elif filter_x == 'Detailed Stats':
				data_dump = pandas.DataFrame( requests.get('https://trackcorona.live/api/countries').json()['data'] )
				locations: list = st.multiselect(label = 'Select Countries', default = ['India', 'United States'],
					options = [country for country in data_dump.location.unique()] )
				st.write(f"** > Selected Countries are ** {', '.join(locations)} ")
				dataset = data_dump if len(locations) == 0 else data_dump[ (data_dump.location.isin( locations )) ]
				st.write('** Stats = ** Total Cases : {} | Total Deaths : {} | Total Recovered : {} '.format(
					int(dataset.confirmed.sum()), int(dataset.dead.sum()), int(dataset.recovered.sum()) ))
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				## Show DataFrame & Map
				st.dataframe( data = dataset )
				st.map( data = dataset, zoom = 2)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Stock Ticker':
		try:
			st.subheader('** Stock Ticker **')
			col_1, col_2, col_3 = st.beta_columns((2, 2, 2))
			companies = pandas.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
			companies.rename(columns = {'Security': 'Company_Name', 'GICS Sector': 'Industry', 
				'GICS Sub-Industry': 'Sub_Industry', 'Headquarters Location': 'Headquaters_Location'}, inplace = True)
			companies = companies[['Symbol', 'Company_Name', 'Industry', 'Sub_Industry', 'Headquaters_Location']]
			company = col_1.selectbox(label = 'Choose Company Name', options = list(set(companies.Company_Name.unique())) )
			company_code = companies[ companies.Company_Name == company ].Symbol.values.tolist()[0].strip()
			st.write(f'** Company Name | Code : ** { company.title() } | { company_code } ')
			start_date: str = col_2.date_input(label = 'Start Date', value = (datetime.today() - timedelta(days = 30)) )
			end_date: str = col_3.date_input(label = 'End Date', value = datetime.today() )
			dataset = yf.download( tickers = company_code.upper(), start = start_date, end = end_date, progress = False )
			st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
			dataset.reset_index( inplace = True )
			dataset.set_index( keys = 'Date', inplace = True )
			parameters = st.multiselect(label = 'Select Parameters', options = list(dataset.columns), default = ['Close'], )
			st.line_chart( dataset[parameters] if len(parameters) > 0 else chart_data['Close'] )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Urban Dictionary':
		try:
			st.subheader('** Urban Dictionary **')
			st.write('Urban Dictionary is a CrowdSourced Online Dictionary For Slang Words and Phrases.')
			keyword: str = st.text_input(label = 'Enter Keyword', value = 'Ghetto')
			response = requests.get(f'https://api.urbandictionary.com/v0/define?term={keyword.lower()}')
			for data in response.json()['list']:
				with st.beta_expander(label = f"Definition = { data.get('definition', 'TBD') } ", expanded = False):
					st.write(f"** Word : ** { data.get('word', 'TBD') } ")
					st.write(f"** Definition : ** { data.get('definition', 'TBD') } ")
					st.write(f"** Example : ** { data.get('example', 'TBD') } ")
					st.write(f"** Thumps Up : ** { data.get('thumbs_up', 'TBD') } ")
					st.write(f"** Thumps Down : ** { data.get('thumbs_down', 'TBD') } ")
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Best Poetries':
		try:
			st.subheader('** Best Poetries **')
			response_1 = requests.get('http://poetrydb.org/author').json()
			author = st.selectbox(label = 'Choose Author', options = response_1['authors'] )
			response_2 = requests.get(f'http://poetrydb.org/author/{author}/author,title,lines,linecount')
			for data in response_2.json():
				with st.beta_expander(label = f"Title = { data.get('title', 'TBD') } ", expanded = False):
					st.write(f"** Title = ** { data.get('title', 'TBD') } ")
					st.write(f"** Author = ** { data.get('author', 'TBD') } ")
					st.write(f'** Poet : **')
					for line in data['lines']:	st.write(line)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'YouTube Downloader':
		try:
			st.subheader('** YouTube Audio / Video Downloader **')
			youtube_link: str = st.text_input(label = 'Paste your YouTube Video URL')
			video_id: str = youtube_link.split('=')[-1] if '/watch' in youtube_link else youtube_link.split('/')[-1]
			dataset: dict = YouTube_Downloader( video_id = video_id )
			with st.beta_expander(label = 'Video Details', expanded = False):
				st.write(f"** Video Title : ** { dataset.get('Title', 'TBD') } ")
				st.write(f"** Video Rating : ** { dataset.get('Rating', 'TBD') } ")
				st.write(f"** Video View Count : ** { dataset.get('ViewCount', 'TBD') } ")
				st.write(f"** Video Author : ** { dataset.get('Author', 'TBD') } ")
				st.write(f"** Video Length : ** { dataset.get('Length', 'TBD') } ")
				st.write(f"** Video Duration : ** { dataset.get('Duration', 'TBD') } ")
				st.write(f"** Video Category : ** { dataset.get('Category', 'TBD') } ")
				st.write(f"** Video Likes : ** { dataset.get('Likes', 'TBD') } ")
				st.write(f"** Video DisLikes : ** { dataset.get('Dislikes', 'TBD') } ")
			with st.beta_expander(label = 'Play YouTube Video', expanded = False):
				Play_YTVideo = f'https://youtube.com/embed/{video_id}'
				st.markdown(f"<iframe width = 400 height = 350 src = '{ Play_YTVideo }' frameborder = 0 allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen> </iframe>", 
					unsafe_allow_html = True)
			with st.beta_expander(label = 'Download Videos', expanded = False):
				for video in dataset['videos']:
					st.write(f"** Resolution : {video.get('Resolution', 'TBD')} | Extension : {video.get('Extension', 'TBD')} | Size: {video.get('FileSize', 'TBD')} **")
					st.markdown(f"<a href = '{video.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Video >> </a>", unsafe_allow_html = True)
			with st.beta_expander(label = 'Download Audios', expanded = False):
				for audio in dataset['audios']:
					st.write(f"** Extension : {audio.get('Extension', 'TBD')} | Size: {audio.get('FileSize', 'TBD')} **")
					st.markdown(f"<a href = '{audio.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Audio >> </a>", unsafe_allow_html = True)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Cloud Market Cost':
		try:
			st.subheader('** Cloud Market Cost **')
			col_1, col_2, col_3, col_4, col_5 = st.beta_columns((2, 2, 2, 2, 2))
			providers: dict = {'Alibaba': 'alibaba', 'Amazon AWS': 'amazon', 'Google GCP': 'google', 'Microsoft Azure': 'azure'}
			provider: str = col_1.selectbox( label = 'Choose Cloud Provider', options = list(providers.keys()) )
			dataset = pandas.DataFrame( Cloud_Market_Cost( provider = providers.get(provider) ) )
			adv_filter: str = col_2.selectbox(label = 'Advanced Filter ?', options = ('Yes', 'No') )
			if adv_filter == 'No':
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			else:
				input_cpu = col_3.selectbox(label = 'Choose CPU', options = list( range(1, 201) ) )
				input_memory = col_4.selectbox(label = 'Choose RAM Memory ', options = list( range(1, 1001) ) )
				input_region = col_5.selectbox(label = 'Choose Region', options = list(set(dataset.Region_Name.unique())) )
				if input_cpu and input_memory and input_region:
					dataset = dataset[ (dataset.CPU <= int(input_cpu)) & (dataset.Memory <= float(input_memory)) &\
						(dataset.Region_Name == input_region) ]
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'AWS Cloud Cost':
		try:
			st.subheader('** AWS Cloud Cost **')
			st.write(' AWS Offers Reliable, Scalable, and Inexpensive Cloud Computing Services. Free to Join, Pay Only for What You Use.')
			st.write(' Please Refer https://aws.amazon.com/blogs/aws/new-aws-price-list-api/ ')
			BASE_URL, dataset = 'https://pricing.us-east-1.amazonaws.com', []
			services = requests.get(f'{BASE_URL}/offers/v1.0/aws/index.json').json()
			services = {data['offerCode'] : data['currentVersionUrl'] for data in list(services['offers'].values())}
			service: str = st.selectbox(label = 'Choose AWS Service', options = list(services.keys()))
			if service in list(services.keys()):
				service_resp = requests.get(f'{BASE_URL}{services[service]}', timeout = 3600).json()
				service_terms, service_products = service_resp['terms']['OnDemand'], service_resp['products']
				for sku in list(service_terms.keys()):
					if sku in list(service_products.keys()):
						products_data = service_products[ sku ]
						terms_data = list(list(service_terms[sku].values())[0]['priceDimensions'].values())[0]
						dataset.append({
							'Service_Name': products_data['attributes'].get('servicename', 'TBD'),
							'Description': terms_data.get('description', 'TBD'),
							'SKU': sku.upper(), 'Unit': terms_data.get('unit', 'TBD'),
							'Cost_Per_Hour': round( float(terms_data['pricePerUnit']['USD']), 2),
							'Product_Family': 'TBD' if not('productFamily' in list(products_data['attributes'].keys())) else products_data['attributes']['productFamily'],
							'Location': 'TBD' if not('location' in list(products_data['attributes'].keys())) else products_data['attributes']['location'],
							'Locations_Type': 'TBD' if not('locationType' in list(products_data['attributes'].keys())) else products_data['attributes']['locationType'],
						})
			st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
			st.dataframe( data = pandas.DataFrame( data = dataset ) )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'National Today':
		try:
			st.subheader('** National Today **')
			st.write('List of Fun holidays and Special Moments on this Cultural Calendar..')
			month_name: str = st.selectbox(label = 'Choose Month', options = [calendar.month_name[i] for i in range(1, 13)])
			dataset = pandas.read_html(f'https://nationaltoday.com/{month_name.lower()}-holidays/')[0]
			st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
			st.dataframe( data = pandas.DataFrame( data = dataset ) )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Google News':
		try:
			st.subheader('** Google News **')
			col_1, col_2, col_3 = st.beta_columns((2, 2, 2))
			keyword: str = col_1.text_input(label = 'Enter Keyword', value = 'Programming')
			start_date: str = col_2.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 30)) )
			end_date: str = col_3.date_input(label = 'End Date', value = datetime.now() )
			if keyword and start_date and end_date:
				googlenews = GoogleNews(lang = 'en', encode = 'utf-8', 
					start = start_date.strftime('%m/%d/%Y'), end = end_date.strftime('%m/%d/%Y'))
				googlenews.search( keyword.upper() )
				for data in googlenews.result():
					with st.beta_expander(label = f"Title = { data.get('title', 'TBD') }", expanded = False):
						st.write(f"** Title : ** { data.get('title', 'TBD') } ")
						st.write(f"** Media / Published Date : ** { data.get('media', 'TBD') } / { data.get('date', 'TBD') } ")
						st.write(f"** Description : ** { data.get('desc', 'TBD') } ")
						st.markdown( f"<a href = '{ data['link'] }' target = '_blank'> More Details, Click Here! </a> ", unsafe_allow_html = True)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Other Tools':
		try:
			st.subheader('** Other Tools **')
			col_1, col_2 = st.beta_columns((2, 2))
			TOOLS = ('Random Password Generator', 'Secure Hash Algorithms', 'QR Code Generator')
			Tool: str = col_1.selectbox(label = 'Choose Tool', options = TOOLS)
			if Tool == 'Random Password Generator':
				input_length: int = col_2.number_input(label = 'Choose the Length', min_value = 6,
					max_value = 20, value = 8, step = 1)
				result: str = ''.join( random.choice(string.digits + string.ascii_lowercase + \
					string.ascii_uppercase + string.punctuation) for i in range(input_length) )
				st.write(f'** Result : ** { result }')
			elif Tool == 'Secure Hash Algorithms':
				st.write('''** Secure Hash Algorithms ** (SHA) are Set of Cryptographic Hash Functions Defined 
					By The Language To Be Used For Various Applications Such as Password Security etc..''')
				keyword: str = col_2.text_input(label = 'Enter the Keyword to Hash', value = 'Programming')
				st.write(f'** Input Keyword : ** { keyword }')
				st.write(f'** SHA 1 : ** { hashlib.sha1(keyword.encode()).hexdigest() }')
				st.write(f'** SHA 224 : ** { hashlib.sha224(keyword.encode()).hexdigest() }')
				st.write(f'** SHA 256 : ** { hashlib.sha256(keyword.encode()).hexdigest() }')
				st.write(f'** SHA 384 : ** { hashlib.sha384(keyword.encode()).hexdigest() }')
				st.write(f'** SHA 512 : ** { hashlib.sha512(keyword.encode()).hexdigest() }')
				st.write(f'** MD5 : ** { hashlib.md5(keyword.encode()).hexdigest() }')
			elif Tool == 'QR Code Generator':
				keyword: str = col_2.text_area(label = 'Enter Text / URL', value = 'Programming', height = 5)
				output = BytesIO()
				img = qrcode.make( keyword )
				img.save( output )
				processed_data = output.getvalue()
				st.image( image = processed_data, width = 300, use_column_width = False )
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'World Countries':
		try:
			st.subheader('** World Countries **')
			col_1, col_2 = st.beta_columns((2, 2))
			BASE_URL: str = 'https://developers.google.com/public-data/docs/canonical/{}'
			filter_x: str = col_1.selectbox(label = 'World Countries / USA States ?', options = ('Countries', 'USA States') )
			request_url = BASE_URL.format('countries_csv') if filter_x == 'Countries' else BASE_URL.format('states_csv')
			dataset = pandas.read_html( request_url )[0]
			dataset.dropna(axis = 0, inplace = True)
			if filter_x == 'Countries':
				countries = col_2.multiselect(label = 'Select World Countries', 
					options = list(dataset.name.unique()), default = ['United States', 'India'] )
				dataset = dataset[ dataset.name.isin( countries ) ]
			elif filter_x == 'USA States':
				usa_states = col_2.multiselect(label = 'Select USA States', 
					options = list(dataset.name.unique()), default = ['California'] )
				dataset = dataset[ dataset.name.isin( usa_states ) ]
			st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
			st.map( data = dataset, zoom = 2)
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'Song Lyrics':
		try:
			st.subheader('** Song Lyrics **')
			col_1, col_2 = st.beta_columns((2, 2))
			artist_name: str = col_1.text_input('Enter Artist Name', value = 'Eminem')
			song_name: str = col_2.text_input('Enter Song Name', value = 'Not Afraid')
			if artist_name and song_name:
				artist_name, song_name = artist_name.title().strip(), song_name.title().strip()
				response = requests.get(f'https://api.lyrics.ovh/v1/{artist_name}/{song_name}').json()
				st.write(f'** Artist Name | Song Name : ** { artist_name } | { song_name }')
				for line in response['lyrics'].split('\n'):
					st.write(line)
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'Text Analysis':
		try:
			st.subheader('** Text Analysis **')
			col_1, col_2, col_3 = st.beta_columns((2, 2, 2))
			language = { value: key for key, value in LANGUAGES.items() }
			choice: str = col_1.radio(label = 'Choose Type', options = ('Language Detection', 'Language Translation', 
				'Sentiment Analysis', 'Spelling Correction', 'Synonyms Antonyms',) )
			sentence = col_2.text_input(label = 'Type Sentence', value = 'Great')
			blob = TextBlob( sentence.strip().title() )
			if choice == 'Language Detection':
				st.write(f'** Language Detected -> ** { language[ blob.detect_language() ] }')
			elif choice == 'Language Translation':
				lang_name = col_3.selectbox(label = 'Choose Language to Translate', options = list(LANGUAGES.keys()) )
				st.write(f"** { sentence.title() } -> ** { blob.translate(to = LANGUAGES[lang_name]) }")
			elif choice == 'Spelling Correction':
				st.write(f"** { sentence.title() } -> ** { blob.correct() }")
			elif choice == 'Sentiment Analysis':
				polarity, subjectivity = blob.sentiment
				polarity, subjectivity = round(float(polarity), 2), round(float(subjectivity), 2)
				sentiment = 'Positive' if polarity >= 0.1 else 'Negative' if polarity <= -0.1 else 'Neutral'
				st.write(f"** { sentence.title() } -> ** { sentiment }")
				st.write(f'** Score -> ** Polarity : { polarity } | Subjectivity : { subjectivity } ')
			elif choice == 'Synonyms Antonyms':
				synonyms, antonyms, text_word = set(), set(), Word( sentence.title() )
				st.write(f'** Word Definition -> ** { text_word.definitions }')
				for synset in text_word.synsets:
					for lemma in synset.lemmas():
						if lemma.antonyms():
							antonyms.add( lemma.antonyms()[0].name() )
						synonyms.add( lemma.name() )
				st.write(f'** Synonyms : ** { synonyms }')
				st.write(f'** Antonyms : ** { antonyms }')
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'Emojis Search':
		try:
			st.subheader('** Emojis Search **')
			col_1, col_2 = st.beta_columns((2, 2))
			filter_x: str = col_1.selectbox(label = 'Search by Category / Tag Name ?', options = ('Category', 'Tag') )
			if filter_x == 'Category':
				categories: list = col_2.multiselect(label = 'Select Emoji Categories', options = list(emojis.db.get_categories()), 
					default = list(emojis.db.get_categories())[-3 : -1] )
				dataset: list = [{
					'Emoji_Name': data.aliases[0], 'Emoji': data.emoji, 'Emoji_Tags': data.tags, 'Category': data.category
				} for category in categories for data in emojis.db.get_emojis_by_category( category ) ]
			else:
				tags: list = col_2.multiselect(label = 'Select Emoji Tags', options = list(emojis.db.get_tags()), 
					default = list(emojis.db.get_tags())[-3 : -1] )
				dataset: list = [{
					'Emoji_Name': data.aliases[0], 'Emoji': data.emoji, 'Emoji_Tags': data.tags, 'Category': data.category
				} for tag in tags for data in emojis.db.get_emojis_by_tag( tag ) ]
			st.markdown( body = Excel_Downloader( pandas.DataFrame( dataset ) ), unsafe_allow_html = True)
			st.dataframe( data = pandas.DataFrame( dataset ) )
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')

	elif CATEGORY == 'Microsoft Learn':
		try:
			st.subheader('** Microsoft Learn **')
			st.write('The Microsoft Learn Catalog API Lets You Send a Web-Based Query to Microsoft Learn and Get \
				Back Details About Published Content Such as Titles, Products Covered, and Links to the Training.')
			response = requests.get('https://docs.microsoft.com/api/learn/catalog').json()
			section: str = st.selectbox(label = 'Select Section', options = list(response.keys()) )
			st.markdown( body = Excel_Downloader( pandas.DataFrame( response[ section ] ) ), unsafe_allow_html = True)
			st.dataframe( data = pandas.DataFrame( response[ section ] ) )
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')

	elif CATEGORY == 'Cricket IPL Stats':
		try:
			st.subheader('** Cricket IPL Stats **')
			col_1, col_2 = st.beta_columns((2, 2))
			options: list = [data for data in range(2008, datetime.now().year + 1)]
			options.append('all-time')
			category: str = col_1.selectbox(label = 'Select IPL Year / All-Time ?', options = options)
			BASE_URL: str = f'https://iplt20.com/stats/{category}'
			ipl_categories: list = ['IPL Winners', 'Most Runs', 'Most Sixes', 'Most Sixes in Innings', 'Highest Scores', 
				'Points Table', 'Best Strike Rate', 'Best Strike Rate in Innings', 'Best Batting Average', 'Most Fifties', 
				'Most Centuries', 'Most Fours', 'Fastest Fifties', 'Fastest Centuries', 'Most Wickets', 'Best Bowling in Innings', 
				'Most Dot Balls', 'Best Bowling Average', 'Best Bowling Economy', 'Most Runs Conceded', 'Most Maiden Overs', 
				'Most 4 Wickets', 'Best Bowling Average Strike Rate in Innings', 'Best Bowling Average Strike Rate' ]
			ipl_categories.sort()
			ipl_category: str = col_2.selectbox(label = 'Select IPL Category', options = ipl_categories )
			if ipl_category == 'IPL Winners':
				st.write('** IPL Winners **')
				dataset = pandas.read_html( requests.get('https://sportskeeda.com/cricket/ipl-winners-list', 
					headers = { 'User-Agent': UserAgent().random }).text )[0]
				new_header = dataset.iloc[0] 
				dataset = dataset[1 : ] 
				dataset.columns = new_header
			elif ipl_category == 'Most Runs':	dataset = pandas.read_html(f'{BASE_URL}/most-runs')[0]
			elif ipl_category == 'Most Sixes':	dataset = pandas.read_html(f'{BASE_URL}/most-sixes')[0]
			elif ipl_category == 'Most Sixes in Innings':	dataset = pandas.read_html(f'{BASE_URL}/most-sixes-innings')[0]
			elif ipl_category == 'Highest Scores':	dataset = pandas.read_html(f'{BASE_URL}/highest-scores')[0]
			elif ipl_category == 'Best Strike Rate':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate')[0]
			elif ipl_category == 'Best Strike Rate in Innings':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate-innings')[0]
			elif ipl_category == 'Best Batting Average':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-average')[0]
			elif ipl_category == 'Most Fifties':	dataset = pandas.read_html(f'{BASE_URL}/most-fifties')[0]
			elif ipl_category == 'Most Centuries':	dataset = pandas.read_html(f'{BASE_URL}/most-centuries')[0]
			elif ipl_category == 'Most Fours':	dataset = pandas.read_html(f'{BASE_URL}/most-fours')[0]
			elif ipl_category == 'Fastest Fifties':	dataset = pandas.read_html(f'{BASE_URL}/fastest-fifties')[0]
			elif ipl_category == 'Fastest Centuries':	dataset = pandas.read_html(f'{BASE_URL}/fastest-centuries')[0]
			elif ipl_category == 'Most Wickets':	dataset = pandas.read_html(f'{BASE_URL}/most-wickets')[0]
			elif ipl_category == 'Best Bowling in Innings':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-innings')[0]
			elif ipl_category == 'Best Bowling Average':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-average')[0]
			elif ipl_category == 'Best Bowling Economy':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-economy')[0]
			elif ipl_category == 'Best Bowling Average Strike Rate in Innings':	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate-innings')[0]
			elif ipl_category == 'Best Bowling Average Strike Rate':	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate')[0]
			elif ipl_category == 'Most Runs Conceded':	dataset = pandas.read_html(f'{BASE_URL}/most-runs-conceded-innings')[0]
			elif ipl_category == 'Most Dot Balls':	dataset = pandas.read_html(f'{BASE_URL}/most-dot-balls')[0]
			elif ipl_category == 'Most Maiden Overs':	dataset = pandas.read_html(f'{BASE_URL}/most-maidens')[0]
			elif ipl_category == 'Most 4 Wickets':	dataset = pandas.read_html(f'{BASE_URL}/most-four-wickets')[0]
			elif ipl_category == 'Points Table':
				if category == 'all-time':	st.write('** No Point Table for All Time Stats in IPL! **')
				dataset = pandas.read_html(f'https://iplt20.com/points-table/{category}')[0]
				dataset.rename(columns = {'Unnamed: 0': 'Rank', 'Pld': 'Matches', 'Pts': 'Points'}, inplace = True)
				dataset = dataset[['Rank', 'Team', 'Matches', 'Won', 'Lost', 'Tied', 'N/R', 'Net RR', 'Points']]
			st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')

	elif CATEGORY == 'ICC Cricket Stats':
		try:
			st.subheader('** ICC Cricket Stats **')
			BASE_URL: str = 'https://icc-cricket.com/rankings/mens'
			icc_categories: list = ['Test Player Batting Stats', 'Test Player Bowling Stats', 'Test Player All-Rounder Stats',
				'ODI Team Stats', 'ODI Player Batting Stats', 'ODI Player Bowling Stats', 'ODI Player All-Rounder Stats',
				'T20I Team Stats', 'T20I Player Batting Stats', 'T20I Player Bowling Stats', 'T20I Player All-Rounder Stats', 'Test Team Stats']
			icc_categories.sort()
			icc_category: str = st.selectbox(label = 'Select ICC Category', options = icc_categories )
			if icc_category == 'Test Team Stats':	dataset = pandas.read_html(f'{BASE_URL}/team-rankings/test')[0]
			elif icc_category == 'Test Player Batting Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/test/batting')[0]
			elif icc_category == 'Test Player Bowling Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/test/bowling')[0]
			elif icc_category == 'Test Player All-Rounder Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/test/all-rounder')[0]
			elif icc_category == 'ODI Team Stats':	dataset = pandas.read_html(f'{BASE_URL}/team-rankings/odi')[0]
			elif icc_category == 'ODI Player Batting Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/odi/batting')[0]
			elif icc_category == 'ODI Player Bowling Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/odi/bowling')[0]
			elif icc_category == 'ODI Player All-Rounder Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/odi/all-rounder')[0]
			elif icc_category == 'T20I Team Stats':	dataset = pandas.read_html(f'{BASE_URL}/team-rankings/t20i')[0]
			elif icc_category == 'T20I Player Batting Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/t20i/batting')[0]
			elif icc_category == 'T20I Player Bowling Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/t20i/bowling')[0]
			elif icc_category == 'T20I Player All-Rounder Stats':	dataset = pandas.read_html(f'{BASE_URL}/player-rankings/t20i/all-rounder')[0]
			st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'ICC Cricket World Cup Stats':
		try:
			st.subheader('** ICC Cricket World Cup Stats **')
			BASE_URL: str = 'https://cricketworldcup.com/stats'
			icc_categories: list = ['Most Runs', 'Highest Scores', 'Best Batting Average', 'Best Batting Strike Rate', 'Best Batting Strike Rate Innings',
				'Most Centuries', 'Fastest Centuries', 'Most Fifties', 'Fastest Fifties', 'Most Sixes', 'Most Fours', 'Best Bowling Average',
				'Best Bowling Economy', 'Best Bowling Economy Innings', 'Best Bowling Strike Rate', 'Best Bowling Strike Rate Innings', 'Most Wickets',
				'Best Bowling Figures', 'Most Maidens', 'Most Dot Balls', 'Most Dot Balls Innings', 'Best Win Percetage', 'Most Wins', 'Most Losses',
				'Highest Match Aggregate', 'Largest Victories Runs', 'Largest Victories Wickets', 'ICC Cricket World Cup Winners']
			icc_categories.sort()
			icc_category: str = st.selectbox(label = 'Select ICC World Cup Category', options = icc_categories )
			if icc_category == 'ICC Cricket World Cup Winners':
				st.write('** ICC Cricket World Cup Winners **')
				request_url: str = 'https://sportskeeda.com/cricket/cricket-world-cup-winners'
				headers: dict = { 'User-Agent': UserAgent().random }
				dataset = pandas.read_html( requests.get(request_url, headers = headers).text )[0]
				new_header = dataset.iloc[0] 
				dataset = dataset[1 : ] 
				dataset.columns = new_header
			if icc_category == 'Most Runs':	dataset = pandas.read_html(f'{BASE_URL}/most-runs')[0]
			elif icc_category == 'Highest Scores':	dataset = pandas.read_html(f'{BASE_URL}/highest-score')[0]
			elif icc_category == 'Best Batting Average':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-average')[0]
			elif icc_category == 'Best Batting Strike Rate':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate')[0]
			elif icc_category == 'Best Batting Strike Rate Innings':	dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate-innings')[0]
			elif icc_category == 'Most Centuries':	dataset = pandas.read_html(f'{BASE_URL}/most-centuries')[0]
			elif icc_category == 'Fastest Centuries':	dataset = pandas.read_html(f'{BASE_URL}/fastest-centuries')[0]
			elif icc_category == 'Most Fifties':	dataset = pandas.read_html(f'{BASE_URL}/most-fifties')[0]
			elif icc_category == 'Fastest Fifties':	dataset = pandas.read_html(f'{BASE_URL}/fastest-fifties')[0]
			elif icc_category == 'Most Sixes':	dataset = pandas.read_html(f'{BASE_URL}/most-sixes')[0]
			elif icc_category == 'Most Fours':	dataset = pandas.read_html(f'{BASE_URL}/most-fours')[0]
			elif icc_category == 'Most Wickets':	dataset = pandas.read_html(f'{BASE_URL}/most-wickets')[0]
			elif icc_category == 'Best Bowling Average':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-average')[0]
			elif icc_category == 'Best Bowling Economy':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-economy')[0]
			elif icc_category == 'Best Bowling Economy Innings':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-economy-innings')[0]
			elif icc_category == 'Best Bowling Strike Rate':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate')[0]
			elif icc_category == 'Best Bowling Strike Rate Innings':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate-innings')[0]
			elif icc_category == 'Best Bowling Figures':	dataset = pandas.read_html(f'{BASE_URL}/best-bowling-figures')[0]
			elif icc_category == 'Most Maidens':	dataset = pandas.read_html(f'{BASE_URL}/most-maidens')[0]
			elif icc_category == 'Most Dot Balls':	dataset = pandas.read_html(f'{BASE_URL}/most-dot-balls')[0]
			elif icc_category == 'Most Dot Balls Innings':	dataset = pandas.read_html(f'{BASE_URL}/most-dot-balls-innings')[0]
			elif icc_category == 'Best Win Percetage':	dataset = pandas.read_html(f'{BASE_URL}/best-win-percentage')[0]
			elif icc_category == 'Most Wins':	dataset = pandas.read_html(f'{BASE_URL}/most-wins')[0]
			elif icc_category == 'Most Losses':	dataset = pandas.read_html(f'{BASE_URL}/most-losses')[0]
			elif icc_category == 'Highest Match Aggregate':	dataset = pandas.read_html(f'{BASE_URL}/highest-match-aggregates')[0]
			elif icc_category == 'Largest Victories Runs':	dataset = pandas.read_html(f'{BASE_URL}/largest-victories-runs')[0]
			elif icc_category == 'Largest Victories Wickets':	dataset = pandas.read_html(f'{BASE_URL}/largest-victories-wickets')[0]
			st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.error(f'\n ** Error: { ex } **')

	elif CATEGORY == 'Weather Report':
		try:
			st.subheader('** Weather Report **')
			city_name = st.text_input(label = 'Enter City Name (NOT Country Name)', value = 'Chennai')
			BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}'
			response = requests.get( BASE_URL.format(city_name.lower(), '28a31767a1909138a53410a56233a326') ).json()
			st.markdown(f"<img src = 'http://openweathermap.org/img/wn/{response['weather'][0]['icon']}.png' width = 75 height = 75 />", 
				unsafe_allow_html = True)
			st.write(f"** City Name : ** { response.get('name', 'TBD') } ")
			st.write(f"** Coordinates : ** Latitude = { response['coord']['lat'] } | Longitude = { response['coord']['lon'] } ")
			st.write(f"** Description : ** { response['weather'][0].get('description', 'TBD').title() } ")
			st.write(f"** Temperature : ** { response['main'].get('temp', 'TBD') } F ")
			st.write(f"** Humidity : ** { response['main'].get('humidity', 'TBD') } ")
			st.write(f"** Wind Speed : ** { response['wind'].get('speed', 'TBD') }" )
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')

	elif CATEGORY == 'Open Trivia':
		try:
			st.subheader('** Open Trivia **')
			col_1, col_2 = st.beta_columns((2, 2))
			BASE_URL: str = 'https://opentdb.com/api.php?amount={}&difficulty={}&type=multiple'
			limit: int = col_1.slider(label = 'How Many Questions ?', min_value = 1, max_value = 50, value = 10, step = 1)
			difficulty: str = col_2.selectbox(label = 'Choose Difficulty', options = ('Easy', 'Medium', 'Hard') )
			dataset = requests.get( BASE_URL.format(limit, difficulty.lower()) ).json()
			for data in dataset['results']:
				with st.beta_expander(label = f"Question = { data.get('question', 'TBD') } ", expanded = False):
					st.write(f"** Category | Difficulty : ** { data.get('category', 'TBD') } | { data.get('difficulty', 'TBD').title() } ")
					st.write(f"** Question : ** { data.get('question', 'TBD') } "),
					st.write(f"** Correct Answer : ** { data.get('correct_answer', 'TBD') } ")
					st.write(f"** InCorrent Answers : ** { data.get('incorrect_answers', 'TBD') } ")
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')

	elif CATEGORY == 'Proxy List':
		try:
			st.subheader('** Proxy List **')
			col_1, col_2 = st.beta_columns((2, 2))
			st.write('''A proxy list is a list of open HTTP/HTTPS/SOCKS proxy servers all on one website. 
				Proxies allow users to make indirect network connections to other computer network services.''')
			dataset = Proxy_List( urls = ['https://sslproxies.org/', 'https://free-proxy-list.net/'] )
			param_1: str = col_1.selectbox(label = 'Choose Parameter', options = ['ALL', 'Country', 'Anonymity', 'Https'] )
			if param_1 == 'ALL':
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			else:
				sub_params: list = [ data for data in dataset[ param_1 ].unique() ]
				param_2: list = col_2.multiselect(label = f'Select { param_1 }', options = sub_params, default = sub_params )
				st.markdown( body = Excel_Downloader( dataset[ dataset[ param_1 ].isin( param_2 ) ] ), unsafe_allow_html = True)
				st.dataframe( data = dataset[ dataset[ param_1 ].isin( param_2 ) ] )
		except Exception as ex:
			st.error(f'\n ** Error: {ex} **')


#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#