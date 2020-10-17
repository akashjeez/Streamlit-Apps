__author__ = 'akashjeez'

import os, sys, re, math, json, time
import random, string, base64, requests
from datetime import datetime, timedelta
from io import BytesIO, TextIOWrapper
import pandas, numpy
import streamlit as st
import yfinance as yf
from googletrans import Translator

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('Ak@$h😎J€€Z')

#----------------------------------------------------------------------------------------------------------------------#

CATEGORIES_LIST: list = ['Age Calculator', 'Python Tutorial', 'Google Translator', 'CoronaVirus Stats',
	'Stock Ticker', 'Urban Dictionary', ]
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
			try:
				for data in response.json()['list']:
					st.write(f"** Word : ** { data.get('word', 'TBD') } ")
					st.write(f"** Definition : ** { data.get('definition', 'TBD') } ")
					st.write(f"** Example : ** { data.get('example', 'TBD') } ")
					st.write(f"** Thumps Up : ** { data.get('thumbs_up', 'TBD') } ")
					st.write(f"** Thumps Down : ** { data.get('thumbs_down', 'TBD') } ")
					st.write('*' * 100)
			except:	raise Exception('Enter Input Urban Word to Get Meaning!')	
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#