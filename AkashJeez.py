__author__ = 'akashjeez'

## Import the Necessary Python Modules.

try:
	import os, sys, math, re, time, copy
	import json, random, string, base64
	import calendar, emojis, qrcode, hashlib
	import requests, pafy, pandas, numpy
	import wikipedia, wikiquote, feedparser
	import streamlit as st
	import yfinance as yf
	from GoogleNews import GoogleNews
	from textblob import TextBlob, Word
	from itertools import chain
	from lxml import html
	import PIL, phonenumbers
	from phonenumbers import timezone, geocoder, carrier
	from io import BytesIO, StringIO, TextIOWrapper
	from functools import reduce
	from datetime import datetime, timedelta
	from dateutil.parser import parse
	from googletrans import Translator
	from bs4 import BeautifulSoup as soup
	from fake_useragent import UserAgent
	from allrecipes import AllRecipes
	from gtts import gTTS
	from PyPDF4 import PdfFileReader, PdfFileWriter
except Exception as ex:
    st.write(f'** Module Error ** : { ex }')

#--------------------------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config( page_title = 'Ak@$h😎J€€Z', page_icon = '🔥', layout = 'wide', initial_sidebar_state = 'auto' )

st.title(body = 'Ak@$h😎J€€Z')

#--------------------------------------------------------------------------------------------------------------------------------------#

CATEGORIES: dict = {
	'Catalog': None,
	'Education': ('Abbrevation Search', 'CDN Libraries', 'Computer Tutorials', 'GitHub Repository', 'Learn Languages', 
		'Linux Tutorial', 'AWS Cloud Cost', 'Programming Notes', 'Programming Rank', 'Python Packages Rank', 'Real Python', 
		'Search Code', 'Stackoverflow Info', 'Tamil Thirukural', 'Technology Cheat Sheet', 'Cheatography', ),
	'Entertainment': ('Coding Jokes', 'India Live TV', 'Movie Database', 'TV Show Search', 'Movie Subtitles',),
	'Food & Drinks': ('CocktailDB', 'Fruits Info', 'Food Recipes', 'Meals Recipes', 'Open BrewaryDB', 'Zomato Search', ),
	'Movies': ('Disney Movies Info', 'English Movies 1', 'English Movies 2', 'Hindi Movies', 'Latest Movies', 'Movie Rankings', 
		'Movie Search Info', 'Tamil Dubbed Movies', 'Tamil Movies 1', 'Tamil Movies 2', 'Visu Movies', ),
	'Songs': ('Apple iTune Musics', 'Audio Database', 'English Album Songs 1', 'English Album Songs 2', 'English MP3 Songs', 
		'English Video Songs', 'Hindi MP3 Songs', 'Latest MP3 Songs', 'Kannada MP3 Songs', 'Malayalam MP3 Songs', 'Online Radio 1', 
		'Online Radio 2', 'Song Lyrics', 'Tamil God MP3 Songs', 'Tamil MP3 Songs', 'Tamil Video Songs', ),
	'Sports': ('Canada Football', 'Cricket Player Stats', 'Sports Database', 'Sport Stats', 'Sports News', ),
	'Useful': ('Age Calculator', 'Bank IFSC Code', 'Best Poetries', 'Bitcoin Price', 'Cloud Market Cost', 'Coin Market Cap',
		'CoVaccine India', 'Coronavirus Stats', 'Currency Exchange', 'Docker Rest API', 'DuckDuckGo Search', 'Emojis Search', 
		'Forbes Billionaires', 'Fuel Price', 'Fuel Price India', 'GSM Arena', 'Gold Silver Price', 'Google Map Search', 'Google News 1', 
		'Google News 2', 'Google Search', 'Google Translator', 'Indian Railways', 'Instagram BOT', 'Job Portal', 'Live News', 
		'Love Calculator', 'Microsoft Learn', 'NBA Stats V2', 'National Today', 'Open Trivia', 'OpenWhyd', 'Other Tools', 
		'Phone Number Tracker', 'Protect PDF', 'Proxy List', 'Python Tutorial', 'Send Free SMS', 'Social Media Stats', 
		'Song Lyrics', 'Stock Ticker', 'Streamlit Apps', 'Temperature', 'Text Analysis', 'Text to Speech', 'Urban Dictionary', 
		'Verify Phone Number', 'Wikipedia Search', 'WikiQuote', 'Weather Report', 'World Countries', 'Youtube Downloader', ),
}

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

#--------------------------------------------------------------------------------------------------------------------------------------#

def Convert_Size(size_bytes: int) -> str:
	if size_bytes == 0:	return '0 B'
	size_name: tuple = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
	i: int = int(math.floor(math.log(size_bytes, 1024)))
	p: float = math.pow(1024, i)
	s: float = round(size_bytes / p, 2)
	return f'{s} {size_name[i]}'


@st.cache
def Bitcoin_Price(timespan: str) -> list:
	BASE_URL: str = 'https://api.blockchain.info/charts'
	response: dict = requests.get(f'{BASE_URL}/market-price?timespan={timespan}&format=json').json()
	dataset: list = [{'Date': datetime.fromtimestamp(data['x']).strftime('%d-%b-%Y'), 
		'Value': data.get('y', 0)} for data in response['values']]
	return dataset


@st.cache
def Crypto_Currencies(currency: str, start_date: str, end_date: str):
	BASE_URL: str = f"https://coinmarketcap.com/currencies/{currency.replace(' ', '-')}"
	request_url: str = BASE_URL + f'/historical-data/?start={start_date}&end={end_date}'
	dataset_1 = pandas.read_html( request_url )[2]
	dataset_1['Date'] = pandas.to_datetime(dataset_1.Date)
	dataset_1.set_index('Date', inplace = True)
	dataset_2 = pandas.read_html( request_url )[3]
	return dataset_1, dataset_2


@st.cache
def Coronavirus_Dataset() -> pandas.DataFrame:
	dataset = pandas.read_excel('https://covid.ourworldindata.org/data/owid-covid-data.xlsx')
	dataset.dropna(subset = ['continent'], inplace = True)
	dataset.date = pandas.to_datetime( dataset.date, infer_datetime_format = True)
	return dataset


@st.cache
def Coronavirus_Dataset_India() -> pandas.DataFrame:
	response: dict = requests.get('https://api.rootnet.in/covid19-in/stats/latest').json()
	dataset = pandas.DataFrame( response['data']['regional'] )
	dataset.rename(columns = {'loc': 'State', 'totalConfirmed': 'Confirmed', 
		'discharged': 'Recovered', 'deaths': 'Deaths'}, inplace = 'TRUE')
	return dataset[['State', 'Confirmed', 'Recovered', 'Deaths']]


@st.cache
def YouTube_Downloader(video_id: str) -> dict:
	video = pafy.new( video_id )
	dataset: dict = {
		'Title': video.title, 'Rating': video.rating, 'ViewCount': video.viewcount,
		'Author': video.username, 'Length': video.length, 'Duration': video.duration,
		'Category': video.category, 'Likes': video.likes, 'Dislikes': video.dislikes, 
	}
	video_dataset: list = [{
		'Resolution': stream.resolution, 'Extension': stream.extension.upper(),
		'FileSize': Convert_Size( stream.get_filesize() ),'DownloadLink': stream.url,
	} for stream in video.videostreams ]
	audio_dataset: list = [{
		'Extension': stream.extension.upper(), 'DownloadLink': stream.url,
		'FileSize': Convert_Size( stream.get_filesize() ), 
	} for stream in video.audiostreams ]
	dataset.update( { 'videos' : video_dataset, 'audios' : audio_dataset } )
	return dataset


@st.cache
def Proxy_List_Dataset(urls: list) -> pandas.DataFrame:
	headers: dict = {'User-Agent': UserAgent().random}
	df_1 = pandas.read_html( requests.get(urls[0], headers = headers).text )[0]
	df_2 = pandas.read_html( requests.get(urls[1], headers = headers).text )[0]
	dataset = df_1.append(df_2, ignore_index = True)
	dataset.drop_duplicates(['IP Address'], inplace = True)
	dataset.dropna(inplace = True)
	return dataset


@st.cache
def Docker_Rest_API(image_name: str) -> dict:
	BASE_URL: str = 'https://hub.docker.com/v2/repositories'
	dataset: dict = requests.get(f'{BASE_URL}/{image_name}?page_size=100').json()
	requests_2: dict = requests.get(f'{BASE_URL}/{image_name}/tags?page_size=100').json()
	pages: int = math.ceil( requests_2['count'] / 100 )
	temp_dataset = requests_2['results'] + list( chain.from_iterable( \
		[requests.get(f'{BASE_URL}/{image_name}/tags?page={i}&page_size=100').json()['results'] for i in range(2, pages + 1)] ) )
	dataset.update( {'tags': temp_dataset } )
	return dataset


@st.cache
def World_Countries(category: str = 'Countries') -> pandas.DataFrame:
	BASE_URL: str = 'https://developers.google.com/public-data/docs/canonical/{}'
	request_url: str = BASE_URL.format('countries_csv') if category == 'Countries' else BASE_URL.format('states_csv')
	dataset = pandas.read_html( request_url )[0]
	dataset.dropna(axis = 0, inplace = True)
	return dataset


@st.cache
def Open_Trivia(limit: int, difficulty: str) -> dict:
	BASE_URL: str = 'https://opentdb.com/api.php?amount={}&difficulty={}&type=multiple'
	dataset: dict = requests.get( BASE_URL.format(limit, difficulty) ).json()
	return dataset.get('results', 'TBD')


@st.cache
def Movie_Subtitles(letter: str) -> dict:
	movie_dataset, BASE_URL = [], 'http://moviesubtitles.org'
	page = soup(requests.get(f'{BASE_URL}/movies-{letter}.html').text, 'lxml')
	for data in page.find_all('a', class_= 'ma'):
		movie_dataset.append({
			'movie_name': data.find('div', class_ = 'mname').text.strip(),
			'movie_year': data.find('div', class_ = 'myear').text.strip(),
			'movie_url': f"{BASE_URL}/{data.get('href', 'TBD')}"
		})
	return {'count': len(movie_dataset), 'data': movie_dataset}


@st.cache
def List_NBA_Players(team_name: str) -> dict:
    try:
        BASE_URL, dataset = 'https://balldontlie.io/api', []
        temp_resp: dict = requests.get(f'{BASE_URL}/v1/players').json()
        total_pages: int = temp_resp.get('meta', 'TBD').get('total_pages', 1)
        for i in range(1, int(total_pages) + 1):
            response: dict = requests.get(f'{BASE_URL}/v1/players?page={i}').json()
            for data in response['data']:
                if data['team']['full_name'] == team_name:
                    data_dump: dict = {
                        'player_id': data.get('id', 'TBD'),
                        'player_name': f"{ data.get('first_name', 'TBD') } {data.get('last_name', 'TBD') }",
                        'height_feet': data.get('height_feet', 'TBD') if 'height_feet' in data.keys() and data['height_feet'] is not None else 'TBD',
                        'height_inches': data.get('height_inches', 'TBD') if 'height_inches' in data.keys() and data['height_inches'] is not None else 'TBD',
                        'weight_pounds': data.get('weight_pounds', 'TBD') if 'weight_pounds' in data.keys() and data['weight_pounds'] is not None else 'TBD',
                        'position': data.get('position', 'TBD') if 'position' in data.keys() and data['position'] is not None else 'TBD',
                    }
                    data_dump.update( data.get('team') )
                    dataset.append( data_dump )
        return dataset
    except Exception as ex:
        return { 'error' : ex }


@st.cache
def Cloud_Cost_Dataset(provider: str) -> pandas.DataFrame:
	dataset, BASE_URL  = [], 'https://banzaicloud.com/cloudinfo/api/v1'
	regions_data: dict = requests.get(f'{BASE_URL}/providers/{provider}/services/compute/regions', timeout = 300).json()
	regions_data: list = [{'id': data['id'], 'name': data['name']} for data in regions_data]
	for region in regions_data:
		request_url: str = f"{BASE_URL}/providers/{provider}/services/compute/regions/{region['id']}/products"
		response: dict = requests.get(request_url, timeout = 300).json()
		if 'products' in response.keys():
			if len(response['products']) > 0:
				for product in response['products']:
					dataset.append({
						'provider': provider,
						'category': product.get('category', 'TBD'), 
						'instance_type': product.get('type', 'TBD'),
						'cpu': int(product.get('cpusPerVm', 0)),
						'memory': round(float(product.get('memPerVm', 0)), 2),
						'cost_per_hour': round(float(product.get('onDemandPrice', 0)), 3),
						'region_id': region.get('id', 'TBD'),
						'region_name': region.get('name', 'TBD'),
						'network_performance': product.get('ntwPerf', 'TBD'),
						'network_perf_category': product.get('ntwPerfCategory', 'TBD'),
					})
	data_dump: dict = {'count': len(dataset), 'data': dataset}
	return pandas.DataFrame( data_dump['data'] )


@st.cache
def Forbes_Billionaires() -> [dict, pandas.DataFrame]:
	response: dict = requests.get(f'https://forbes400.herokuapp.com/api/forbes400/getAllBillionaires').json()
	dataset: list = [{
		'Rank': data.get('rank', 'TBD'), 'Name': data.get('personName', 'TBD'),
		'NetWorth': f" { round(data.get('finalWorth', 0.00) / 1000, 2) } Billion",
		'Source': data.get('source', 'TBD'), 'Industries': data.get('industries', 'TBD'), 
		'Image': f"https:{data.get('squareImage', 'TBD')}" if 'squareImage' in data.keys() else 'TBD', 
		'State': data.get('state', 'TBD'), 'City': data.get('city', 'TBD'), 
		'BirthDate': (datetime(1970, 1, 1) + timedelta(seconds = (data.get('birthDate')/1000) ))\
			.strftime('%d-%b-%Y') if data.get('birthDate') else 'TBD', 
		'Country': data.get('countryOfCitizenship', 'TBD'),
		'Gender': 'Male' if data.get('gender') == 'M' else 'Female',
		'Biography': data.get('bios', 'TBD'), 'Abouts': data.get('abouts', 'TBD')
	} for data in response]
	return response, pandas.DataFrame( dataset )


@st.cache
def Instagram_Bot(insta_url: str) -> dict:
	try:
		page = soup(requests.get(url = insta_url).text, 'lxml')
		match = re.search(r'window\._sharedData = (.*);</script>', str(page))
		resp_json: dict = json.loads(match.group(1))
		raw_data: dict = resp_json['entry_data']['ProfilePage'][0]['graphql']['user']
		dataset: dict = {
			'user_id': raw_data.get('id', 'TBD'),
			'username': raw_data.get('username', 'TBD'),
			'full_name': raw_data.get('full_name', 'TBD'),
			'followers': raw_data['edge_followed_by'].get('count', 'TBD') 
				if 'edge_followed_by' in raw_data.keys() else 'TBD',
			'followering': raw_data['edge_follow'].get('count', 'TBD') 
				if 'edge_follow' in raw_data.keys() else 'TBD',
			'external_url': raw_data.get('external_url', 'TBD'),
			'biography': raw_data.get('biography', 'TBD'),
			'profile_pic': raw_data.get('profile_pic_url', 'TBD'),
			'profile_pic_hd': raw_data.get('profile_pic_url_hd', 'TBD'),
			'private_account': 'No' if raw_data.get('is_private', 'TBD') == False else 'Yes',
			'verified_account': 'No' if raw_data.get('is_verified', 'TBD') == False else 'Yes',
			'joined_recently': 'No' if raw_data.get('is_joined_recently', 'TBD') == False else 'Yes',
			'business_account': 'No' if raw_data.get('is_business_account', 'TBD') == False else 'Yes',
			'posts': [{
				'post_id': data.get('node', 'TBD').get('id', 'TBD'),
				'display_url': data.get('node', 'TBD').get('display_url', 'TBD'),
				'accessibility_caption': data.get('node', 'TBD').get('accessibility_caption', 'TBD'),
				'creation_date': datetime.fromtimestamp(int(data['node']['taken_at_timestamp'])).strftime('%d-%b-%Y %I:%M %p'), 
				'caption': data.get('node', 'TBD').get('edge_media_to_caption', 'TBD').get('edges', 'TBD'),
				'resolution': data.get('node', 'TBD').get('dimensions', 'TBD'),
			} for data in raw_data['edge_owner_to_timeline_media']['edges']],
			'video_posts': [{
				'video_post_id': data.get('node', 'TBD').get('id', 'TBD'),
				'title': data.get('node', 'TBD').get('title', 'TBD'),
				'like_count': data.get('node', 'TBD').get('edge_liked_by', 'TBD').get('count', 'TBD'),
				'location': data.get('node', 'TBD').get('location', 'TBD'),
				'video_duration': data.get('node', 'TBD').get('video_duration', 'TBD'),
				'video_view_count': data.get('node', 'TBD').get('video_view_count', 'TBD'),
				'creation_date': datetime.fromtimestamp(int(data['node']['taken_at_timestamp'])).strftime('%d-%b-%Y %I:%M %p'),
				'caption': data.get('node', 'TBD').get('edge_media_to_caption', 'TBD').get('edges', 'TBD'),
				'resolution': data.get('node', 'TBD').get('dimensions', 'TBD'),
			} for data in raw_data['edge_felix_video_timeline']['edges']],
		}
		return dataset
	except Exception as ex:
		return { 'error' : ex }    


def Excel_Downloader(df):
	output = BytesIO()
	writer = pandas.ExcelWriter(output, engine = 'xlsxwriter')
	df.to_excel(writer, sheet_name = 'Data')
	writer.save()
	processed_data = output.getvalue()
	b64 = base64.b64encode(processed_data)
	return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"


#--------------------------------------------------------------------------------------------------------------------------------------#

def Execute_Main() -> None:

	with st.sidebar:
		st.warning(body = '[ <BuyMeACoffee>] ( https://buymeacoffee.com/akashjeez ) If you like it.')
		with st.expander(label = 'About Me', expanded = False):
			st.info(body = '''
				Developed by AkashJeez :) \n
				Feel Free to Reach Out to Me Via \n
				[ << Blogspot >>  ] ( https://akashjeez.blogspot.com/ ) \n
				[ << Instagram >> ] ( https://instagram.com/akashjeez/ ) \n
				[ << Twitter >>   ] ( https://twitter.com/akashjeez/ ) \n
				[ << GitHub >>    ] ( https://github.com/akashjeez/ ) \n
				[ << Dev.to >>    ] ( https://dev.to/akashjeez/ ) \n
				[ << Medium >>    ] ( https://akashjeez.medium.com/ ) \n
				[ << Wordpress >> ] ( https://akashjeez.wordpress.com/ ) \n
				[ << LinkedIn >>  ] ( https://linkedin.com/in/akash-ponnurangam-408363125/ ) \n
			''')
		with st.expander(label = 'Other Apps', expanded = False):
			st.warning(body = '''
				Learn Programming Tutorials (Python, Julia, Go, R) \n
				[ << App 1 >>  ] ( https://pyphilonoist.herokuapp.com/ )
			''')
		with st.expander(label = 'Share this App', expanded = False):
			st.info(body = '''
				[ << Facebook >>  ] ( https://facebook.com/sharer/sharer.php?u=https://akashjeez.herokuapp.com/ ) \n
				[ << Whatsapp >>  ] ( https://wa.me/?text=https://akashjeez.herokuapp.com/ ) \n
				[ << Twitter >>   ] ( https://twitter.com/share?url=https://akashjeez.herokuapp.com/&text=Akashjeez ) \n
				[ << Google + >>  ] ( https://plus.google.com/share?url=https://akashjeez.herokuapp.com/ ) \n
				[ << LinkedIn >>  ] ( https://linkedin.com/shareArticle?url=https://akashjeez.herokuapp.com/&title=Akashjeez ) \n
				[ << Tumblr >>    ] ( https://tumblr.com/share/link?url=https://akashjeez.herokuapp.com/&name=Akashjeez ) \n
				[ << Wordpress >> ] ( https://wordpress.com/press-this.php?u=https://akashjeez.herokuapp.com/&t=Akashjeez ) \n
				[ << Reddit >>    ] ( https://reddit.com/submit?url=https://akashjeez.herokuapp.com/&title=Akashjeez ) \n
			''')

	col_1, col_2, col_3 = st.columns((2, 2, 2))
	CATEGORY: str = col_1.selectbox(label = 'Choose Category', options = list(CATEGORIES.keys()) )
	st.write('*' * 50)

	if CATEGORY == 'Catalog':
		st.write('** Catalog ** Page Shows the List of Micro Apps Based on Category & Sub-Category in this Web Application.')
		st.table( data = [{'CATEGORY': key, 'SUB_CATEGORY': data} for key, value in CATEGORIES.items() \
			if value is not None for data in value] )


	elif CATEGORY == 'Education':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )
		
		if SUB_CATEGORY == 'Abbrevation Search':
			try:
				st.subheader('** Abbrevation Search **')
				keyword: str = st.text_input(label = 'Enter Keyword', value = '')
				if keyword is not None and len( keyword ) > 0:
					response = soup(requests.get(f'http://acronyms.silmaril.ie/cgi-bin/xaa?{keyword.upper()}').text, 'lxml')
					st.write(f'** Input Keyword = ** { keyword.upper() } ')
					for data in [str(data.text) for data in response.find_all('expan')]:
						st.write(f'** Result ** --> { data } ')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'CDN Libraries':
			try:
				st.subheader('** CDN Libraries **')
				st.write('** CDN JS ** is a Library Repository Which Hosted on Cloudflare.com. Its Freely Available CDN for \
					Common Javascript and CSS libraries. Such Type of System Mostly Known as CDN (Content Delivery Network). \
					CDNJS Host Mostly Known Production Ready Versions of JavaScript/CSS Library. The Goal is to Deliver \
					Content Easily to End-users with High Availability and High Performance.')
				response: dict = requests.get('https://api.cdnjs.com/libraries').json()
				if 'results' in response.keys() and len( response['results'] ) > 0:
					data_dump: list = [{
						'Name': data.get('name', 'TBD'), 'CDN Link': data.get('latest', 'TBD'),
					} for data in response.get('results') ]
					st.markdown( body = Excel_Downloader( pandas.DataFrame( data = data_dump ) ), unsafe_allow_html = True)
					st.dataframe( data = pandas.DataFrame( data = data_dump ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Computer Tutorials':
			try:
				st.subheader('** Computer Tutorials **')
				dataset, BASE_URL = [], 'https://tuto-computer.com'
				page = soup(markup = requests.get(url = BASE_URL).text, features = 'lxml')
				for data1 in page.find_all('ul')[1].find_all('li'):
					page_2 = soup(requests.get(url = f"{BASE_URL}{data1.a.get('href', 'TBD')[1:]}").text, 'lxml')
					for data2 in page_2.find_all('article', class_ = 'item-list'):
						PDF_Name: str = data2.a.get('title', 'TBD').split('Download ')[-1].split(' course')[0].strip()
						Download_Link: str = f"{BASE_URL}/download-file-{data2.a.get('href').split('/')[-1].split('-')[0]}.html"
						st.markdown(body = f'''
							<li> PDF Name = { PDF_Name } | <a href = '{ Download_Link }' target = '_blank'> Download Link </a> </li>
						''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'GitHub Repository':
			try:
				st.subheader('** GitHub Repository **')
				username: str = st.text_input(label = 'Enter GitHub Username', value = 'akashjeez')
				if username is not None and len( username ) > 0:
					response: dict = requests.get(url = f'https://api.github.com/users/{username.lower()}').json()
					st.markdown( f"<img class = 'rounded-circle article-img' src='{response.get('avatar_url', 'TBD')}' \
						width = 200 height = 200>", unsafe_allow_html = True )
					st.write(f"** GitHub ID : ** {response.get('id', 'TBD')} ")
					st.write(f"** GitHub User Full Name : ** {response.get('name', 'TBD')} ")
					st.write(f"** Account Created : ** { datetime.strptime(response['created_at'], '%Y-%m-%dT%H:%M:%S%fZ').strftime('%d-%m-%Y') } ")
					st.markdown(f"** GitHub User URL : ** <a href = '{response.get('html_url', 'TBD')}' target = '_blank'> {response.get('html_url', 'TBD')} </a> ", unsafe_allow_html = True)
					st.write(f"** Repositories Count : ** {response.get('public_repos', 'TBD')} ")
					st.markdown(f"** Repository URL : ** <a href = '{response.get('repos_url', 'TBD')}' target = '_blank'> {response.get('repos_url', 'TBD')} </a> ", unsafe_allow_html = True)
					with st.expander(label = 'List Repositories', expanded = False):
						for response in requests.get(url = f'https://api.github.com/users/{username.lower()}/repos').json():
							if st.checkbox(label = f"Repository Name = { response.get('name', 'TBD') } "):
								st.write(f"** Repository ID : ** {response.get('id', 'TBD')} ")
								st.write(f"** Repository Name : ** {response.get('name', 'TBD')} ")
								st.write(f"** Repository Full Name : ** {response.get('full_name', 'TBD')} ")
								st.write(f"** Language Used : ** {response.get('language', 'TBD')} ")
								st.markdown(body = f"** Repository URL : ** <a href = '{response.get('html_url', 'TBD')}' target = '_blank'> \
									{response.get('html_url', 'TBD')} </a> ", unsafe_allow_html = True)
								st.write(f"** Repository Description : ** {response.get('description', 'TBD')} ")
								st.write(f"** Repository Created Date : ** {datetime.strptime(response['created_at'], '%Y-%m-%dT%H:%M:%S%fZ').strftime('%d-%m-%Y')} ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Learn Languages':
			try:
				st.subheader('** Learn Languages **')
				dataset, BASE_URL = [], 'http://ilanguages.org'
				col_1, col_2 = st.columns((2, 2))
				Language_List = reduce(lambda x,y: x + y, pandas.read_html(f'{BASE_URL}/index.php')[0].values.tolist())
				Languages = Language_List[ : len( Language_List ) - 1]
				Languages.remove('English')
				Language_Name: str = col_1.selectbox(label = 'Select Language Name', options = Languages)
				Language_Type: str = col_2.selectbox(label = 'Select Language Type', options = ('Grammer', 'Phrases', 'Vocabulary') )
				for Language in Languages:
					if Language == Language_Name:
						page = soup(requests.get(f'{BASE_URL}/{Language.lower()}_{Language_Type.lower()}.php').text, 'lxml')
						for data in page.find_all('td')[8:-10]:
							if len( data ) > 0:
								st.write(f'** { data.big.text } | { data.dfn.text } **')
								st.markdown(body = f'''<audio controls = 'controls' preload = 'auto'> 
									<source src = "{BASE_URL}/{data.audio.get('src')}" type = 'audio/mpeg'> 
									</audio>''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Linux Tutorial':
			try:
				st.subheader('** Linux Tutorial **')
				with st.expander(label = 'Tutorial', expanded = False):
					st.markdown(body = '''
						<b> What is Linux? </b>
		 				<p> Linux is the best-known and most-used open source operating system. As an operating system, Linux is software that sits underneath all of the other software on a computer, receiving requests from those programs and relaying these requests to the computer’s hardware. <br/> For the purposes of this page, we use the term “Linux” to refer to the Linux kernel, but also the set of programs, tools, and services that are typically bundled together with the Linux kernel to provide all of the necessary components of a fully functional operating system. Some people, particularly members of the Free Software Foundation, refer to this collection as GNU/Linux, because many of the tools included are GNU components. However, not all Linux installations use GNU components as a part of their operating system. Android, for example, uses a Linux kernel but relies very little on GNU tools. </p>
		 				<b> How does Linux differ from other operating systems? </b>
		 				<p> In many ways, Linux is similar to other operating systems you may have used before, such as Windows, OS X, or iOS. Like other operating systems, Linux has a graphical interface, and types of software you are accustomed to using on other operating systems, such as word processing applications, have Linux equivalents. In many cases, the software’s creator may have made a Linux version of the same program you use on other systems. If you can use a computer or other electronic device, you can use Linux. <br/> But Linux also is different from other operating systems in many important ways. First, and perhaps most importantly, Linux is open source software. The code used to create Linux is free and available to the public to view, edit, and—for users with the appropriate skills—to contribute to. Linux is also different in that, although the core pieces of the Linux operating system are generally common, there are many distributions of Linux, which include different software options. This means that Linux is incredibly customizable, because not just applications, such as word processors and web browsers, can be swapped out. Linux users also can choose core components, such as which system displays graphics, and other user-interface components. </p>
		 				<b> What is the difference between Unix and Linux? </b>
		 				<p> You may have heard of Unix, which is an operating system developed in the 1970s at Bell Labs by Ken Thompson, Dennis Ritchie, and others. Unix and Linux are similar in many ways, and in fact, Linux was originally created to be similar to Unix. Both have similar tools for interfacing with the systems, programming tools, filesystem layouts, and other key components. However, Unix is not free. Over the years, a number of different operating systems have been created that attempted to be “unix-like” or “unix-compatible,” but Linux has been the most successful, far surpassing its predecessors in popularity. </p>
		 				<b> Who uses Linux? </b>
		 				<p> You're probably already using Linux, whether you know it or not. Depending on which user survey you look at, between one- and two-thirds of the webpages on the Internet are generated by servers running Linux. <br/> Companies and individuals choose Linux for their servers because it is secure, and you can receive excellent support from a large community of users, in addition to companies like Canonical, SUSE, and Red Hat, which offer commercial support. <br/> Many of the devices you own probably, such as Android phones, digital storage devices, personal video recorders, cameras, wearables, and more, also run Linux. Even your car has Linux running under the hood. </p>
		 				<b> Who owns Linux? </b>
		 				<p> By virtue of its open source licensing, Linux is freely available to anyone. However, the trademark on the name “Linux” rests with its creator, Linus Torvalds. The source code for Linux is under copyriopy( data )ght by its many individual authors, and licensed under the GPLv2 license. Because Linux has such a large number of contributors from across multiple decades of development, contacting each individual author and getting them to agree to a new license is virtually impossible, so that Linux remaining licensed under the GPLv2 in perpetuity is all but assured. </p>
		 				<b> How was Linux created? </b>
		 				<p> Linux was created in 1991 by Linus Torvalds, a then-student at the University of Helsinki. Torvalds built Linux as a free and open source alternative to Minix, another Unix clone that was predominantly used in academic settings. He originally intended to name it “Freax,” but the administrator of the server Torvalds used to distribute the original code named his directory “Linux” after a combination of Torvalds’ first name and the word Unix, and the name stuck. </p>
		 				<b> How can I contribute to Linux? </b>
		 				<p> Most of the Linux kernel is written in the C programming language, with a little bit of assembly and other languages sprinkled in. If you’re interested in writing code for the Linux kernel itself, a good place to get started is in the Kernel Newbies FAQ, which will explain some of the concepts and processes you’ll want to be familiar with. </p>
		 				<b> How can I get started using Linux? </b>
		 				<p> There's some chance you're using Linux already and don’t know it, but if you’d like to install Linux on your home computer to try it out, the easiest way is to pick a popular distribution that is designed for your platform (for example, laptop or tablet device) and give it a shot. Although there are numerous distributions available, most of the older, well-known distributions are good choices for beginners because they have large user communities that can help answer questions if you get stuck or can’t figure things out. Popular distributions include Debian, Fedora, Mint, and Ubuntu, but there are many others. </p>
					''', unsafe_allow_html = True)
				with st.expander(label = 'Commands', expanded = False):
					dataset, headers = [], {'User-Agent': UserAgent().random }
					response = requests.get('https://fossbytes.com/a-z-list-linux-command-line-reference/', headers = headers)
					for i in range(0, 26):
						dataset += pandas.read_html(response.text)[i].values.tolist()
					dataset = [{'Command': data[0], 'Description': data[1]} for data in dataset]
					st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
					st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'AWS Cloud Cost':
			try:
				st.subheader('** AWS (Amazon Web Services) Cloud Cost **')
				st.write('AWS Offers Reliable, Scalable, and Inexpensive Cloud Computing Services. Free to Join, Pay Only for What You Use.')
				st.write('Please Refer https://aws.amazon.com/blogs/aws/new-aws-price-list-api/ ')
				BASE_URL, dataset = 'https://pricing.us-east-1.amazonaws.com', []
				services: dict = requests.get(url = f'{BASE_URL}/offers/v1.0/aws/index.json').json()
				services: dict = { data['offerCode'] : data['currentVersionUrl'] for data in list(services['offers'].values()) }
				service: str = st.selectbox(label = 'Choose AWS Service', options = list(services.keys()))
				if service in list(services.keys()):
					service_resp: dict = requests.get(f'{BASE_URL}{services[service]}', timeout = 3600).json()
					service_terms, service_products = service_resp['terms']['OnDemand'], service_resp['products']
					for sku in list(service_terms.keys()):
						if sku in list(service_products.keys()):
							products_data = service_products[sku]
							terms_data: list = list(list(service_terms[sku].values())[0]['priceDimensions'].values())[0]
							dataset.append({
								'Service_Name': products_data['attributes'].get('servicename', 'TBD'),
								'Description': terms_data.get('description', 'TBD'),
								'SKU': sku, 'Unit': terms_data.get('unit', 'TBD'),
								'Cost_Per_Hour': round( float(terms_data['pricePerUnit']['USD']), 2),
								'Product_Family': 'TBD' if not('productFamily' in list(products_data['attributes'].keys())) else products_data['attributes']['productFamily'],
								'Location': 'TBD' if not('location' in list(products_data['attributes'].keys())) else products_data['attributes']['location'],
								'Locations_Type': 'TBD' if not('locationType' in list(products_data['attributes'].keys())) else products_data['attributes']['locationType']
							})
				st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
				st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Programming Notes':
			try:
				st.subheader('** Programming Notes **')
				BASE_URL: str = 'https://books.goalkicker.com'
				page = soup(requests.get(url = BASE_URL).text, 'lxml')
				for data in page.find_all('div', class_ = 'bookContainer grow'):
					st.markdown(body = f'''
						<b> PDF Title = </b> { data.img.get('alt', 'TBD').title() } | 
						<a href = "{BASE_URL}/{data.a.get('href')}{data.a.get('href').replace('Book/', '')}\
							NotesForProfessionals.pdf" target = '_blank'> Download Link </a>''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Programming Rank':
			try:
				st.subheader('** Programming Rank **')
				dataset = pandas.read_html('http://statisticstimes.com/tech/top-computer-languages.php')
				with st.expander(label = 'Rank Worldwide', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[2] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[2] )
				with st.expander(label = 'Rank USA', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[3] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[3] )
				with st.expander(label = 'Rank India', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[4] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[4] )
				with st.expander(label = 'Rank Germany', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[5] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[5] )
				with st.expander(label = 'Rank UK', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[6] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[6] )
				with st.expander(label = 'Rank France', expanded = False):
					st.markdown( body = Excel_Downloader( dataset[7] ), unsafe_allow_html = True)
					st.dataframe( data = dataset[7] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Python Packages Rank':
			try:
				st.subheader('** Python Packages Rank **')
				col_1, col_2 = st.columns((2, 2))
				BASE_URL: str = 'https://hugovk.github.io/top-pypi-packages'
				Durations: dict = { '1 Month': '30-days', '1 Year': '365-days' }
				Duration: str = col_1.selectbox(label = 'Last 1 Month / 1 Year ?', options = list(Durations.keys()) )
				limit: int = col_2.slider(label = 'Select Limit', min_value = 10, max_value = 4000, step = 10)
				response: dict = requests.get(url = f"{BASE_URL}/top-pypi-packages-{Durations[Duration]}.json").json()
				dataset: list = [{
					'Rank': index + 1, 'Download_Count': data.get('download_count', 'TBD'), 
					'Project_Title': data.get('project', 'TBD'), 'Project_Link': f"https://pypi.org/project/{data['project']}/",
				} for index, data in enumerate( response['rows'] ) ]
				dataset = pandas.DataFrame( data = dataset )[:limit]
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Real Python':
			try:
				st.subheader('** Real Python **')
				dataset, BASE_URL = [], 'https://realpython.com'
				page_1 = soup(requests.get(url = f'{BASE_URL}/tutorials/all/').text, 'lxml')
				page_links: list = [[data.text.strip(), data.get('href')] for data in page_1.find_all('a', class_ = 'stretched-link')]
				page_title: str = st.selectbox(label = 'Select Post Category', options = [page_name for page_name, _ in page_links])
				for page_name, page_link in page_links:
					if page_name == page_title:
						page_2 = soup(requests.get(f"{BASE_URL}{page_link}").text, 'lxml')
						for data in page_2.find_all('div', class_ = 'card border-0'):
							with st.expander(label = data.img.get('alt', 'TBD'), expanded = False):
								st.write(f'** Post Category = ** { page_name } ')
								st.write(f"** Sub Post Category = ** { data.img.get('alt', 'TBD') } ")
								st.write( f"{BASE_URL}{data.a.get('href')}" )
								st.image(image = data.img.get('src', 'TBD'), width = 200, height = 200)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Stackoverflow Info':
			try:
				st.subheader('** Stackoverflow Info **')
				dataset, BASE_URL = [], 'https://api.stackexchange.com/2.2'
				with st.expander(label = 'Info', expanded = False):
					response: dict = requests.get(f'{BASE_URL}/info?site=stackoverflow').json()
					if data := response['items'][0]:
						st.write(f"** Total Users = ** { data.get('total_users', 'TBD') } ")
						st.write(f"** Total Questions = ** { data.get('total_questions', 'TBD') } ")
						st.write(f"** Total Answers = ** { data.get('total_answers', 'TBD') } ")
						st.write(f"** Total Accepted = ** { data.get('total_accepted', 'TBD') } ")
						st.write(f"** Total UnAnswered = ** { data.get('total_unanswered', 'TBD') } ")
						st.write(f"** Answers Per Minute = ** { data.get('answers_per_minute', 'TBD') } ")
						st.write(f"** Questions Per Minute = ** { data.get('questions_per_minute', 'TBD') } ")
						st.write(f"** Badges Per Minute = ** { data.get('badges_per_minute', 'TBD') } ")
						st.write(f"** Total Votes = ** { data.get('total_votes', 'TBD') } ")
						st.write(f"** Total Badges = ** { data.get('total_badges', 'TBD') } ")
						st.write(f"** Total Comments = ** { data.get('total_comments', 'TBD') } ")
				with st.expander(label = 'Posts', expanded = False):
					response: dict = requests.get(f'{BASE_URL}/posts?pagesize=100&order=desc&sort=activity&site=stackoverflow').json()
					for data in response['items']:
						if owner_info := data.get('owner'):
							dataset.append({
								'User_ID': owner_info.get('user_id', 'TBD'), 'User_Type': owner_info.get('user_type', 'TBD').title(),
								'User_Name': owner_info.get('display_name', 'TBD'), 'Profile_Link': owner_info.get('link', 'TBD'),
								'Score': data.get('score', 'TBD'), 'Post_ID': data.get('post_id', 'TBD'),
								'Post_Name': data.get('link', 'TBD'),  'Post_Type': data.get('post_type', 'TBD').title(),
								'Last_activity_Date': datetime.fromtimestamp(data['last_activity_date']).strftime('%d-%m-%Y %H:%M %p') 
									if 'last_activity_date' in data.keys() else 'TBD',
								'Creation_Date': datetime.fromtimestamp(data['creation_date']).strftime('%d-%m-%Y %H:%M %p') 
									if 'creation_date' in data.keys() else 'TBD',
							})
					st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset )), unsafe_allow_html = True)
					st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil Thirukural':
			try:
				st.subheader('** தமிழ் திருக்குறள் **')
				response: dict = requests.get('https://raw.githubusercontent.com/akashjeez/study/master/thirukkural.json').json()
				dataframe: list = pandas.read_html('http://valaitamil.com/thirukkural.php')[2].values.tolist()
				adhigarams: list = [f"{i[0]} - {i[1]} - {i[2]}" for i in dataframe[ 1 : len(dataframe)-1 ]]
				adhigaram = st.selectbox(label = 'Choose அதிகாரம்', options = adhigarams)
				st.write(f'** அதிகாரம் = ** { adhigaram } ')
				for i in range(1, len(adhigarams)+1):
					if i == int(adhigaram.split(' - ')[0]):
						for j in range(i*10-9, i*10+1):
							for data in response['kural']:
								if data['Number'] == j:
									st.write(f"** குறள் = ** { data.get('Number', 'TBD') } ")
									st.write(f" { data.get('Line1', 'TBD') } \n { data.get('Line2', 'TBD') } ")
									st.write(f"** Explanation = ** { data.get('explanation', 'TBD') } ")
									st.write(f"** விளக்கம் = ** { data.get('mk', 'TBD') } ")
									st.write(f"** தமிங்கிலம் = ** \n { data.get('transliteration1', 'TBD') } \n { data.get('transliteration2', 'TBD') } ")
									st.write('*' * 50)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Technology Cheat Sheet':
			try:
				st.subheader('** Technology Cheat Sheet **')
				response: dict = requests.get(url = 'https://api.github.com/repos/akashjeez/cheat-sheets/contents').json()
				file_name: str = st.selectbox(label = 'Select File Name', options = [ data['name'] for data in response ])
				for data in response:
					if data['name'] == file_name:
						st.write(f"** File Name = ** { file_name.upper().split('.')[0] } ")
						st.markdown(body = f"""<a href = "{data['download_url']}"> Download Link </a>""", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Search Code':
			try:
				st.subheader('** Search Code **')
				st.write('** Search Code ** - Simple, Comprehensive Code Search Accross Public Code Sources.')
				col_1, col_2 = st.columns((2, 2))
				query: str = col_1.text_input(label = 'Enter Query', value = 'import numpy')
				per_page: int = col_2.slider(label = 'How Many Results?', min_value = 5, max_value = 100, step = 1)
				if query is not None and per_page is not None:
					response: dict = requests.get(f'https://searchcode.com/api/codesearch_I/?q={query}&per_page={per_page}').json()
					if response.get('total') > 0:
						for index, data in enumerate( response.get('results') ):
							with st.expander(label = f'Result - {index+1}', expanded = False):
								st.json( data )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Cheatography':
			try:
				st.subheader('** Cheatography **')
				st.write('Download Cheat Sheets for Education, Software, Home, Business, Games etc.')
				BASE_URL: str = 'https://cheatography.com'
				col_1, col_2 = st.columns((2, 2))
				Cat_Lev_1: str = col_1.selectbox(label = 'Select Level 1 Category', options = ('Business', 
					'Education', 'Games', 'Home', 'Programming', 'Software') )
				page_1 = soup(requests.get(url = f'{BASE_URL}/{Cat_Lev_1.lower()}').text, 'lxml')
				Temp_Dataset: list = [{'Name': data_2.a.text.strip(), 'Link': data_2.a.get('href', 'TBD') } 
					for data_1 in page_1.find('div', class_ = 'triptych3').find_all('ul')[1:] for data_2 in data_1.find_all('li') ]
				Cat_Lev_2: str = col_2.selectbox(label = 'Select Level 2 Category', options = [i['Name'] for i in Temp_Dataset])
				for data in Temp_Dataset:
					if data['Name'] == Cat_Lev_2:
						st.write(f'** { Cat_Lev_1 } -> { Cat_Lev_2 } **')
						page_2 = soup(requests.get(f"{BASE_URL}{data.get('Link', '/TBD')}").text, 'lxml')
						pages = int(page_2.find('span', class_= 'page_list').find_all('a')[-1].text) + 1 \
							if page_2.find('span', class_= 'page_list') is not None else 2
						for page_num in range(1, pages):
							page_3 = soup(requests.get(f"{BASE_URL}{data.get('Link', '/TBD')}/{page_num}").text, 'lxml')
							for data_2 in page_3.find('div', class_ = 'triptychdbll').find_all('a', {'itemprop': 'url'}):
								with st.expander(label = data_2.text.strip(), expanded = False):
									st.write(f"** PDF Name ** = { data_2.text.strip() }")
									st.write(f"** Download PDF ** = {BASE_URL}{data_2.get('href', '/TBD/')}pdf/ ")			
			except Exception as ex:
				st.error(f'** Error : { ex } **')


	elif CATEGORY == 'Entertainment':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Coding Jokes':
			try:
				st.subheader('** Coding Jokes **')
				page_1 = soup(requests.get(url = 'https://commitstrip.com/en/?').text, 'lxml')
				for data in page_1.find_all('section')[:15]:
					with st.expander(label = data.strong.text.strip(), expanded = False):
						page_2 = soup(requests.get(url = data.a.get('href', 'TBD') ).text, 'lxml')
						st.write(f"** Published Date = ** { page_2.find_all('div', class_='entry-meta')[0].a.time.text } ")
						st.markdown(body = f''' <img src = "{page_2.find_all('div', class_='entry-content')[0].img.get('src', 'TBD')}" \
							width = 300 height = 300> ''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'India Live TV':
			try:
				st.subheader('** India Live TV **')
				Languages: tuple = ('Bengali', 'English', 'Gujarati', 'Hindi', 'Kannada', 'Malayalam', 
					'Marathi', 'Odia', 'Punjabi', 'Tamil', 'Telugu', 'Urdu')
				Language: str = st.selectbox(label = 'Choose Language', options = Languages)
				page_1 = soup(markup = requests.get(url = f'https://tvhub.in/{Language}/').text, features = 'lxml')
				for data in page_1.find_all('li', class_='list-group-item'):
					page_2 = soup(requests.get(url = f"https://tvhub.in{data.a.get('href', 'TBD')}").text, 'lxml')
					st.write(f"** Channel Name = ** { data.text.split('(')[0].strip() } ")
					st.markdown(body = f""" <iframe width = 400 height = 350 src = "{page_2.find('iframe').get('src').split('?')[0]}" \
						frameborder = 0 allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' \
						allowfullscreen> </iframe> """, unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Movie Database':
			try:
				st.subheader('** Movie Database **')
				BASE_URL, API_KEY = 'https://api.themoviedb.org/3', '83b89eb288c22d8bac09793405c79c90'
				st.write('The Movie Database (TMDb) is a Popular, User Editable Database For Movies and TV shows. ')
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				MovieDB_Category: str = col_1.selectbox(label = 'Choose Movie DB Categories', options = ('MovieDB Search', 'Popular Movies',
					'Upcoming Movies', 'Top Rated Movies', 'Now Playing Movies', 'Today Airing TV Shows', 'On the Air - TV Shows',
					'Popular TV Shows', 'Top Rated TV Shows' ))
				if MovieDB_Category == 'MovieDB Search':
					keyword: str = col_2.text_input(label = 'Enter Keyword')
					type_name: str = col_3.selectbox(label = 'Select Type', options = ('movie', 'person', 'tv'))
					if keyword is not None and type_name is not None:
						response = requests.get(f'{BASE_URL}/search/{type_name}?query={keyword}&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Popular Movies':
					response = requests.get(f'{BASE_URL}/movie/popular?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Upcoming Movies':
					response = requests.get(f'{BASE_URL}/movie/upcoming?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Top Rated Movies':
					response = requests.get(f'{BASE_URL}/movie/top_rated?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Now Playing Movies':
					response = requests.get(f'{BASE_URL}/movie/now_playing?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Today Airing TV Shows':
					response = requests.get(f'{BASE_URL}/tv/airing_today?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Popular TV Shows':
					response = requests.get(f'{BASE_URL}/tv/popular?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'Top Rated TV Shows':
					response = requests.get(f'{BASE_URL}/tv/top_rated?&api_key={API_KEY}&language=en-US').json().get('results')
				elif MovieDB_Category == 'On the Air - TV Shows':
					response = requests.get(f'{BASE_URL}/tv/on_the_air?&api_key={API_KEY}&language=en-US').json().get('results')
				dataset = [{
					'ID': data.get('id', 'TBD'), 'Name': data.get('title', 'TBD'), 
					'Overview': data.get('overview', 'TBD'), 'Release_Date': data.get('release_date', 'TBD'),
					'Image_URL': f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{data.get('poster_path', 'TBD')}",
					'Vote_Count': data.get('vote_count', 'TBD'), 'Average': data.get('vote_average', 'TBD'),
					'Popularity': data.get('popularity', 'TBD'), 'First_Air_Date': data.get('first_air_date', 'TBD'),
				} for data in response ]
				st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset )), unsafe_allow_html = True)
				st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'TV Show Search':
			try:
				st.subheader('** TV Show Search **')
				show_name: str = st.text_input(label = 'Enter TV Show Name', value = None)
				if show_name is not None and len( show_name ) > 0:
					response = requests.get(url = f"http://api.tvmaze.com/search/shows?q={show_name.replace(' ','+')}")
					dataset = [{
						'Name': data['show'].get('name', 'TBD'), 'Type': data['show'].get('type', 'TBD'),
						'URL': data['show'].get('url', 'TBD'), 'Language': data['show'].get('language', 'TBD'),
						'Genres': data['show'].get('genres', 'TBD'), 'Summary': data['show'].get('summary', 'TBD'),
						'Country': data['show']['network'].get('country', 'TBD'),
						'IMDB_ID': data['show']['externals'].get('imdb', 'TBD'),
						'Image_Link': data['show']['image'].get('medium', 'TBD'),
					} for data in response.json() ]
					st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset )), unsafe_allow_html = True)
					st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Movie Subtitles':
			try:
				st.subheader('** Movie Subtitles **')
				col_1, col_2 = st.columns((2, 2))
				letters, BASE_URL = list( string.ascii_uppercase + '0' ), 'http://moviesubtitles.org'
				letter: str = col_1.selectbox(label = 'Select Movie Name Letter Starts With ?', options = letters)
				movie_dataset: dict = Movie_Subtitles( letter )['data']
				st.markdown( Excel_Downloader( pandas.DataFrame( movie_dataset ) ), unsafe_allow_html = True)
				st.dataframe( data = movie_dataset )
				movie_names: list = list( set( [movie['movie_name'] for movie in movie_dataset] ) )
				movie_title: str = col_2.selectbox(label = 'Select Movie', options = movie_names)
				for movie in movie_dataset:
					if movie['movie_name'] == movie_title:
						page = soup(requests.get( movie['movie_url'] ).text, 'lxml')
						temp = page.find('a', {'title': 'Download english subtitles'}).find('nobr').text
						download_link = f"{BASE_URL}/files/{movie['movie_name'].replace(' ','_')}_{movie['movie_year']}.{temp}.en.zip"
						st.write(f'** Movie Subtitle Download Link :** { download_link }')
			except Exception as ex:
				st.error(f'** Error : { ex } **')


	elif CATEGORY == 'Food & Drinks':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )
		
		if SUB_CATEGORY == 'CocktailDB':
			try:
				st.subheader('** CocktailDB **')
				dataset, BASE_URL = [], 'https://thecocktaildb.com/api/json/v1/1'
				response_1: dict = requests.get(url = f'{BASE_URL}/list.php?c=list').json()
				Category: str = st.selectbox(label = 'Choose Category', options = [data['strCategory'] for data in response_1['drinks']] )
				response_2 = requests.get(url = f'{BASE_URL}/filter.php?c={Category}', timeout = 6000).json()
				for data in response_2.get('drinks'):
					response_3 = requests.get(url = f"{BASE_URL}/lookup.php?i={data['idDrink']}", timeout = 6000)
					temp_data: dict = response_3.json()['drinks'][0]
					st.write(f"** Drink ID = ** { data.get('idDrink', 'TBD') } **| Drink Name = ** { data.get('strDrink', 'TBD') } ")
					st.image(image = data.get('strDrinkThumb', None), width = 300, height = 300)
					st.write(f"** Category = ** { temp_data.get('strCategory', 'TBD') } **| Glass = ** { temp_data.get('strGlass', 'TBD') } ")
					st.write(f"** Alcholol? = ** { temp_data.get('strAlcoholic', 'TBD') } ")
					st.write(f"** Instructions = ** { temp_data.get('strInstructions', 'TBD') } ")
					st.write( '-' * 50 )			
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Fruits Info':
			try:
				st.subheader('** Fruits Info **')
				page_1 = soup(requests.get(url = 'https://halfyourplate.ca/fruits-and-veggies/fruits-a-z/').text, 'lxml')
				fruits_info: list = [[data.find_all('a')[1].text, data.find_all('a')[0].get('href')] 
					for data in page_1.find_all('ul', class_ = 'fv-list')[0].find_all('li')]
				del fruits_info[54] ## 'prickly-pear'
				fruit_title: str = st.selectbox(label = 'Choose Fruit Name', options = [fruit_name for fruit_name,_ in fruits_info])
				for fruit_name, fruit_link in fruits_info:
					if fruit_title == fruit_name:
						st.write(f"** Fruit Name = ** { fruit_name } ")
						page_2 = soup(requests.get(url = fruit_link).text, 'lxml')
						st.image(image = page_2.find_all('div', class_ = 'entry')[0].img.get('src', 'TBD'), width = 200)
						if page_2.find('span', class_ = 'cta-blue'):
							st.markdown(body = f'''<a href = {page_2.find('span', class_ = 'cta-blue').a.get('href')} \
								target_ = '_blank'> Download PDF </a>''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Food Recipes':
			try:
				st.subheader('** Food Recipes **')
				dish_name: str = st.text_input(label = 'Enter Dish Name', value = '')
				if dish_name is not None and len( dish_name ) > 0:
					query_result = AllRecipes.search(query_dict = {'wt': dish_name.lower(), 'sort': 're'})
					for recipe in query_result:
						with st.expander(label = recipe.get('name', 'TBD'), expanded = False):
							st.write(f"** Recipe Name = ** { recipe.get('name') } ")
							st.write(f"** Recipe Description = ** { recipe.get('description', 'TBD') } ")
							st.image(image = recipe.get('image', 'TBD'), width = 300)
							if data := AllRecipes.get( recipe.get('url', 'TBD') ):
								st.write('** Ingredients are **')
								st.write( ingredient for ingredient in data['ingredients'] )
								st.write('** Cooking Steps **')
								st.write( step for step in data['steps'] )
								st.write('** Preparation / Cooking / Total Time = {} | {} | {} **'.format( \
									data.get('prep_time', 'TBD'), data.get('cook_time', 'TBD'), data.get('total_time', 'TBD') ))
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Open BrewaryDB':
			try:
				st.subheader('** Open Brewary Database **')
				page_num: int = st.number_input(label = 'Choose Page Number', min_value = 1, max_value = 160, step = 1)
				response = requests.get(f'https://api.openbrewerydb.org/breweries?per_page=50&page={page_num}')
				dataset = [{
					'ID': data.get('id', 'TBD'), 'Name': data.get('name', 'TBD'),
					'Type': data.get('brewery_type', 'TBD'), 'Street': data.get('street', 'TBD'),
					'City' : data.get('city', 'TBD'), 'State': data.get('state', 'TBD'),
					'Postal Code': data.get('postal_code', 'TBD'), 'Country': data.get('country', 'TBD'),
					'Latitude': data.get('latitude', 'TBD'), 'Longitude': data.get('longitude', 'TBD'),
					'Phone': data.get('phone', 'TBD'), 'Website_URL': data.get('website_url', 'TBD'),
				} for data in response.json() ]
				st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset )), unsafe_allow_html = True)
				st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Meals Recipes':
			try:
				st.subheader('** Meals Recipes **')
				Meal_IDs, dataset, BASE_URL = [], [], 'https://themealdb.com/api/json/v1/1'
				response_1: dict = requests.get(url = f'{BASE_URL}/list.php?c=list').json()
				category: str = st.selectbox(label = 'Choose Category', options = [i['strCategory'] for i in response_1['meals']])
				response_2: dict = requests.get(f'{BASE_URL}/filter.php?c={category}').json()
				Meal_IDs.append( [ data['idMeal'] for data in response_2['meals'] ] )
				for meal_id in Meal_IDs[0]:
					response_3: dict = requests.get(f'{BASE_URL}/lookup.php?i={meal_id}').json()
					data: dict = response_3['meals'][0]
					youtube_link: str = f"https://youtube.com/embed/{data.get('strYoutube').split('=')[1]}"
					st.write(f"** Meal Name = ** { data.get('strMeal', 'TBD') } ")
					st.image(image = data.get('strMealThumb', 'TBD'), width = 200)
					st.markdown(body = f'''
						<a href = "{data.get('strSource', 'TBD')}" target = '_blank'> Source Link </a>
						<br/> <iframe width = 600 height = 450 src = "{youtube_link}" frameborder = 0 allow = 'accelerometer; \
						autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen> </iframe> ''', unsafe_allow_html = True)
					st.write(f"** Meal Category / Area = ** { data.get('strCategory', 'TBD') }  / { data.get('strArea', 'TBD') }")
					st.write(f"** Meal Insructions = ** { data.get('strInstructions', 'TBD') } ")
					st.write( '*' * 50 )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Zomato Search':
			try:
				st.subheader('** Zomato Search **')
				col_1, col_2 = st.columns((2, 2))
				BASE_URL: str = 'https://developers.zomato.com/api/v2.1'
				headers: dict = {'Accept': 'application/json', 'user-key': 'cfd8808bd0ee9691bf52734c4d43e1bf'}
				city_name, keyword = col_1.text_input(label = 'Enter City Name'), col_2.text_input(label = 'Enter Dish Name')
				if city_name is not None and keyword is not None:
					response_1 = requests.get(f'{BASE_URL}/locations?query={city_name}', headers = headers).json()
					if 'location_suggestions' in response_1.keys() and len( response_1['location_suggestions'] ) > 0:
						data: dict = response_1['location_suggestions'][0]
						entity_type, entity_id = data.get('entity_type', 'TBD'), data.get('entity_id', 'TBD')
						response_2: dict = requests.get(f"{BASE_URL}/search?entity_id={entity_id}&entity_type={entity_type}\
							&q={keyword.replace(' ','+')}", headers = headers).json()
						if 'restaurants' in response_2.keys() and len( response_2['restaurants'] ) > 0:
							for data in response_2['restaurants']:
								if data := data['restaurant']:
									with st.expander(label = data.get('name'), expanded = False):
										st.write(f"** Restaurant ID / Name = ** { data.get('id', 'TBD') } / { data.get('name', 'TBD') } ")
										st.write(f"** Cuisines = ** { data.get('cuisines', 'TBD') } ")
										if data.get('featured_image'):	st.image(image = data.get('featured_image'), width = 300, height = 300)
										st.write(f"** Average Cost Per 2 Persons= ** { data.get('currency') } { data.get('average_cost_for_two') } ")
										st.write(f"** Restaurant Address = ** { data['location'].get('address', 'TBD') } ")
										st.write(f"** Timings / Phone Number = ** { data.get('timings', 'TBD') } / { data.get('phone_numbers', 'TBD') } ")
										st.markdown(body = f'''
											<a href = "{ data.get('book_url') if 'book_url' in data.keys() else 'TBD' }" target_ = 'blank'> Book URL </a> &nbsp;
											<a href = "{ data.get('menu_url') if 'menu_url' in data.keys() else 'TBD' }" target = '_blank'> Menu URL </a>
										''', unsafe_allow_html = True)
										if user_rating := data.get('user_rating'):
											st.write(f"** Restaurant Ratings = ** { user_rating.get('aggregate_rating', 'TBD') } ({ user_rating.get('rating_text', 'TBD') }) ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')


	elif CATEGORY == 'Movies':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Disney Movies Info':
			try:
				st.subheader('** Disney Movies Info **')
				BASE_URL: str = 'https://disneymovieslist.com'
				Disney_Category: str = st.selectbox(label = 'Select Disney Categories', options = ('Animated Movies',
					'Disney Movies', 'Marvel Movies', 'Pixar Movies', 'Disney Theme Parks', 'Disney Hotels & Resorts',
					'USA Box Office', 'opening Weekend Box Office'))
				if Disney_Category == 'Animated Movies':
					request_url: str = BASE_URL + '/list-of-animated-disney-movies/'
				elif Disney_Category == 'Disney Movies':
					request_url: str = BASE_URL + '/list-of-disney-channel-movies/'
				elif Disney_Category == 'Marvel Movies':
					request_url: str = BASE_URL + '/list-of-marvel-movies/'
				elif Disney_Category == 'Pixar Movies':
					request_url: str = BASE_URL + '/list-of-disney-theme-parks/'
				elif Disney_Category == 'Disney Theme Parks':
					request_url: str = BASE_URL + '/list-of-disney-hotels-and-resorts/'
				elif Disney_Category == 'Disney Hotels & Resorts':
					request_url: str = BASE_URL + '/top-25-best-disney-movies-domestic-usa-box-office-sales/'
				elif Disney_Category == 'USA Box Office':
					request_url: str = BASE_URL + '/best-disney-movies-opening-weekend-box-office-performance/'
				st.markdown( body = Excel_Downloader( pandas.read_html( request_url )[0] ), unsafe_allow_html = True)
				st.dataframe( data = pandas.read_html( request_url )[0] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'English Movies 1':
			try:
				st.subheader('** English Movies 1 **')
				Movie_Links, BASE_URL = [], 'https://coolmoviez.casa/movielist'
				for i in range(1, 4):
					page = soup(requests.get(f'{BASE_URL}/13/Hollywood_movies/default/{i}.html').text, 'lxml')
					Movie_Links += [[data.text.split('\n')[0], data.get('href')] for data in page.find_all('a', class_='fileName')]
				Movie_Name: str = st.selectbox(label = 'Select English Movie', options = [movie_name for movie_name, _ in Movie_Links])
				for movie_title, movie_link in Movie_Links:
					if Movie_Name == movie_title:
						page_2 = soup(requests.get( url = movie_link ).text, 'lxml')
						page_3 = soup(requests.get( url = page_2.find_all('a', class_='fileName')[0].get('href') ).text, 'lxml')
						st.write(f'** Movie Name = ** { Movie_Name }')
						if page_2.find('img', class_ = 'absmiddle'):
							st.image(image = page_2.find('img', class_ = 'absmiddle').get('src', 'TBD'), width = 250)
						if page_3.find_all('a', class_ = 'dwnLink'):
							st.markdown(body = f"""<a href = { page_3.find_all('a', class_='dwnLink')[0].get('href', 'TBD') }> \
								Movie Download Page </a>""", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'English Movies 2':
			try:
				st.subheader('** English Movies 2 **')
				BASE_URL, year = 'https://filmyzilla.agency', datetime.now().year
				page_1 = soup(requests.get(f'{BASE_URL}/category/365/New-hollywood-english-movies-{year}/default/1.html').text, 'lxml')
				Movie_List: list = [[data.a.get('title'), data.a.get('href')] for data in \
					page_1.find_all('div', {'class': lambda x: x and x.startswith('movie')} )]
				for movie_name, movie_link in Movie_List:
					with st.expander(label = movie_name, expanded = False):
						page_2 = soup(requests.get( url = movie_link ).text, 'lxml')
						st.image(image = page_2.find('span', class_ = 'imglarge').img.get('src', 'TBD'), width = 250)
						st.markdown(body = f"""<a href = { page_2.find('div', class_= 'listed').a.get('href') }> \
							Movie Download Page </a>""", unsafe_allow_html = True) 
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Hindi Movies':
			try:
				st.subheader('** Hindi Movies **')
				BASE_URL, Year, Movie_Links = 'http://moviespur.com', datetime.now().year, []
				for i in range(1, 3):
					page_1 = soup(requests.get(url = f'{BASE_URL}/category/new-bollywood-movies-146/{i}.html').text, 'lxml')
					Movie_Links += [[data.text.strip(), data.get('href')] for data in page_1.find_all('a', class_ = 'touch')]
				for movie_name, movie_link in Movie_Links:
					with st.expander(label = movie_name, expanded = False):
						page_2 = soup(requests.get(url = f'{ BASE_URL }{ movie_link }').text, 'lxml')
						page_3 = soup(requests.get(f"{BASE_URL}{page_2.find_all('a', class_ = 'touch')[-1].get('href')}").text, 'lxml')
						st.write(f'** Movie Name = ** { movie_name }')
						if image_data := page_2.find('div', class_='folderimage'):
							st.image(image = f"{ BASE_URL }{ image_data.img.get('src', 'TBD') }", width = 250)
						if download_data := page_3.find('a',class_='downloadbutton'):
							st.markdown(body = f"""<a href = { BASE_URL }{ download_data.get('href', 'TBD') }> \
								Download Movie (.MP4) </a>""", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Movie Rankings':
			try:
				st.subheader('** Movie Rankings **')
				BASE_URL: str = 'https://boxofficemojo.com'
				st.write('** Top Lifetime Gross **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/chart/top_lifetime_gross/')[0] )
				st.write('** Top Daily Gross **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/chart/release_top_daily_gross/')[0] )
				st.write('** Show Down **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/showdown/')[0] )
				st.write('** WorldWide Box Office **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/year/world/{datetime.now().year}/')[0] )
				st.write('** Brand **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/brand/')[0] )
				st.write('** Genre **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/genre/')[0] )
				st.write('** Franchise **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/franchise/')[0] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Movie Search Info':
			try:
				st.subheader('** Movie Search Info **')
				movie_name: str = st.text_input(label = 'Enter Movie Name', value = 'Coach Carter')
				if movie_name is not None and len( movie_name ) > 0:
					dataset: dict = requests.get(url = f'http://omdbapi.com/?apikey=80440342&t={movie_name}').json()
					if 'Error' not in dataset.keys():
						st.image(image = dataset.get('Poster', 'TBD'), width = 250)
						st.json( body = dataset )
					else:
						st.warning(' ** Movie Name NOT Found, Please Try Again! ** ')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Latest Movies':
			try:
				st.subheader('** Latest Movies **')
				BASE_URL: str = 'https://movierockers.me'
				for i in range(1, 4):
					page_1 = soup(requests.get(f'{BASE_URL}/search/all/all/all/latest/?page={i}').text, 'lxml')
					for data_1 in page_1.find_all('div', class_= lambda x: x and x.startswith('browse-movie-wrap')):
						movie_name: str = data_1.find_all('a')[-1].text.strip()
						with st.expander(label = movie_name, expanded = False):
							st.write(f'** Movie Name = ** { movie_name } ')
							if data_1.img.get('data-src'):
								st.image(image = data_1.img.get('data-src', 'TBD'), width = 250)
							page_2 = soup(requests.get(f"{ BASE_URL }{ data_1.a.get('href', '/TBD') }").text, 'lxml')
							for data_2 in page_2.find_all('a', {'rel': 'nofollow'}):
								if data_2.get('href').endswith('.torrent'):
									st.markdown(body = f'''<a href = "{ BASE_URL }{ data_2.get('href') }" target_ = '_blank'> \
										Download Torrent File </a>''', unsafe_allow_html = True)
								if data_2.get('href').endswith('.mp4'):
									st.markdown(body = f'''<a href = "{ data_2.get('href') }" target_ = '_blank'> \
										Download Movie (.MP4) </a>''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil Dubbed Movies':
			try:
				st.subheader('** Tamil Dubbed Movies **')
				Movie_Links, Year, BASE_URL = [], datetime.now().year, 'http://madrasdub.com'
				for page_num in range(1, 4):
					page_1 = soup(requests.get(f'{BASE_URL}/tamil/tamil-{Year}-dubbed-movies.html?page={page_num}').text, 'lxml')
					Movie_Links += [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('div', class_='ytg')]
				for movie_name, movie_link in Movie_Links:
					with st.expander(label = movie_name, expanded = False):
						page_2 = soup(requests.get( url = movie_link ).text, 'lxml')
						st.write(f'** Movie Name = ** { movie_name } ')
						if len( page_2.find_all('img') ) > 0:
							st.image(image = f"{BASE_URL}{page_2.find_all('img')[1].get('src', 'TBD')}", width = 250)
						if len( page_2.find_all('div', class_ = 'ytg') ) > 0:
							download_link: str = page_2.find('div', class_='ytg').a.get('href').replace('.html', '.html?download')
							st.markdown(body = f"<a href = {download_link} target = '_blank' download> Download Movie (.MP4) </a>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil Movies 1':
			try:
				st.subheader('** Tamil Movies 1 **')
				Movie_Links, Year, BASE_URL = [], datetime.now().year, 'https://madrasrockerss.vin'
				for page_num in range(1, 5):
					page_1 = soup(requests.get(f'{BASE_URL}/tamil/4768/tamil-{Year}-movies.html?page={page_num}&dir=4768').text, 'lxml')
					Movie_Links += [[data.a.text, data.a.get('href')] for data in page_1.find_all('div', class_ = 'ytg')]
				for movie_name, movie_link in Movie_Links:
					with st.expander(label = movie_name, expanded = False):
						page_2 = soup(requests.get( movie_link ).text, 'lxml')
						page_3 = soup(requests.get( page_2.find('div', class_ = 'ytg').a.get('href') ).text, 'lxml')
						page_4 = soup(requests.get( page_3.find('div', class_ = 'ytg').a.get('href').replace('get', 'show') ).text, 'lxml')
						download_link: str = page_4.find_all('div', class_='downloadnew')[-1].a.get('href')
						st.write(f'** Movie Name = ** { movie_name } ')
						st.write(f"** File ** { page_3.find('div', class_ = 'ytg').b.text.strip() } ")
						st.markdown(body = f"<a href = { download_link } target = '_blank' download> \
							Download Movie (.MP4) </a>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil Movies 2':
			try:
				st.subheader('** Tamil Movies 2 **')
				BASE_URL, Year, Movie_Links = 'http://srirockers.biz', datetime.now().year, []
				for i in range(1, 4):
					page_1 = soup(requests.get(f"{BASE_URL}/tamil-{Year}-movies-download.html?page={i}").text, 'lxml')
					Movie_Links += [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('div', class_ = 'listlinks')]
				for movie_name, movie_link in Movie_Links:
					with st.expander(label = movie_name, expanded = False):
						page_2 = soup(requests.get(url = movie_link).text, 'lxml')
						if page_2.find('div', class_='ytg') is None:	continue
						page_3 = soup(requests.get( page_2.find('div', class_='ytg').a.get('href') ).text, 'lxml')
						st.write(f"** Movie Name = ** { movie_name } ")
						if len( page_2.find_all('img') ) > 0:
							st.image(image = f"{ BASE_URL }{ page_2.find_all('img')[1].get('src', 'TBD') }", width = 250)
						st.write(f"** File Size = ** { page_2.find('div', class_ = 'ytg').find_all('b')[1].text.strip() } ")
						st.markdown(body = f"<a href = { page_3.find('h2').a.get('href') }?download target = '_blank'> \
							Download Movie (.MP4) </a>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Visu Movies':
			try:
				st.subheader('** Visu Movies **')
				st.image(image = 'https://nettv4u.com/imagine/v/i/s/u/0/j/visu.jpg', width = 200)
				st.write(''' Meenakshisundaram Ramasamy Viswanthan (1 July 1945 – 22 March 2020), best known by his stage name Visu, 
					was an Indian writer, director, stage, film and television actor and talk-show host. Visu initially worked as an 
					assistant to director K. Balachander until becoming a director himself. He later began acting, with his first film 
					being Kudumbam Oru Kadambam, directed by S. P. Muthuraman.''')
				st.markdown(body = "** For More Details, <a href = 'https://en.wikipedia.org/wiki/Visu' target ='_blank'> Click Here! </a> **", unsafe_allow_html = True)
				dataset: dict = requests.get(url = 'https://raw.githubusercontent.com/akashjeez/study/master/visu_movies.json').json()
				movie_name: str = st.selectbox(label = 'Select Movie', options = [movie['movie_name'] for movie in dataset['result']] )
				for data in dataset['result']:
					if data['movie_name'] == movie_name:
						st.write(f"** Movie Name : ** {data.get('movie_name', 'TBD')} ")
						st.write(f"** Year / Director : ** {data.get('year', 'TBD')} / {data.get('director', 'TBD')} ")
						st.write(f"** Writer / Actor : ** {data.get('writer', 'TBD')} / {data.get('actor', 'TBD')} ")
						if 'youtube' in data['movie_link'] and 'embed' in data['movie_link']:
							dataset: dict = YouTube_Downloader( video_id = data['movie_link'].split('/')[-1] )
							with st.expander(label = 'Video Details', expanded = False):
								st.write(f"** Video Title : ** { dataset.get('Title', 'TBD') } ")
								st.write(f"** Video Rating : ** { dataset.get('Rating', 'TBD') } ")
								st.write(f"** Video View Count : ** { dataset.get('ViewCount', 'TBD') } ")
								st.write(f"** Video Author : ** { dataset.get('Author', 'TBD') } ")
								st.write(f"** Video Length : ** { dataset.get('Length', 'TBD') } ")
								st.write(f"** Video Duration : ** { dataset.get('Duration', 'TBD') } ")
								st.write(f"** Video Category : ** { dataset.get('Category', 'TBD') } ")
								st.write(f"** Video Likes : ** { dataset.get('Likes', 'TBD') } ")
								st.write(f"** Video DisLikes : ** { dataset.get('Dislikes', 'TBD') } ")
							with st.expander(label = 'Play YouTube Video', expanded = False):
								Play_YTVideo: str = f"https://youtube.com/embed/{ data['movie_link'].split('/')[-1] }"
								st.markdown(body = f"<iframe width = 400 height = 350 src = '{ Play_YTVideo }' frameborder = 0 allow = 'accelerometer; \
									autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen> </iframe>", unsafe_allow_html = True)
							with st.expander(label = 'Download Videos', expanded = False):
								for video in dataset['videos']:
									st.write(f"** Resolution : {video.get('Resolution', 'TBD')} | Extension : {video.get('Extension', 'TBD')} | Size: {video.get('FileSize', 'TBD')} **")
									st.markdown(body = f"<a href = '{video.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Video >> </a>", unsafe_allow_html = True)
							with st.expander(label = 'Download Audios', expanded = False):
								for audio in dataset['audios']:
									st.write(f"** Extension : {audio.get('Extension', 'TBD')} | Size: {audio.get('FileSize', 'TBD')} **")
									st.markdown(body = f"<a href = '{audio.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Audio >> </a>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		
	elif CATEGORY == 'Songs':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Apple iTune Musics':
			try:
				st.subheader('** Apple iTune Musics **')
				artist_name: str = st.text_input(label = 'Enter Artist Name')
				if artist_name is not None:
					artist_name: str = artist_name.replace(' ','+').lower()
					response = requests.get(url = f'https://itunes.apple.com/search?term={artist_name}').json()
					for data in response['results']:
						with st.expander(label = f"Album Name = { data.get('collectionName', 'TBD') }", expanded = False):
							st.image(image = data.get('artworkUrl100', 'TBD'), width = 250)
							st.write(f"** Artist Name = ** { data.get('artistName', 'TBD') } ")
							st.write(f"** Album Name = ** { data.get('collectionName', 'TBD') } ")
							st.write(f"** Song Track Name = ** { data.get('trackName', 'TBD') } ")
							st.write(f"** Artist View URL = ** { data.get('artistViewUrl', 'TBD') } ")
							st.write(f"** Album / Song Track View URL = ** { data.get('collectionViewUrl', 'TBD') } ")
							st.write(f"** Album Price = ** { data.get('collectionPrice', 'TBD') } { data.get('currency', 'TBD') } ")
							st.write(f"** Song Track Price = ** { data.get('trackPrice', 'TBD') } { data.get('currency', 'TBD') } ")
							if 'releaseDate' in data.keys():
								st.write(f"** Release Date = ** { datetime.strptime(data['releaseDate'][:10], '%Y-%m-%d').strftime('%d-%m-%Y') } ")
							st.write(f"** Country = ** { data.get('country', 'TBD') } ")
							st.write(f"** Album Genre = ** { data.get('primaryGenreName', 'TBD') } ")
							st.markdown(body = f"<audio controls> <source src = { data.get('previewUrl', 'TBD') } \
								type = 'audio/mp4'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Audio Database':
			try:
				st.subheader('** Audio Database **')
				col_1, col_2 = st.columns((2, 2))
				BASE_URL: str = 'https://theaudiodb.com/api/v1/json/1'
				artist_name: str = col_1.text_input(label = 'Enter Artist Name')
				adb_category: str = col_2.selectbox(label = 'Select AudioDB Category', options = ('Artist', 'Album'))
				if artist_name is not None and adb_category == 'Artist':
					response = requests.get(url = f'{BASE_URL}/search.php?s={artist_name.strip().lower()}')
					data: dict = response.json()['artists'][0]
					st.write(f"** Artist ID / Name= ** { data.get('idArtist', 'TBD') } / { data.get('strArtist', 'TBD') } ")
					st.image(image = data.get('strArtistThumb', 'TBD'), width = 250)
					st.write(f"** Artist Real Name= ** { data.get('strArtistAlternate', 'TBD') } ")
					st.write(f"** Style / Genre = ** { data.get('strStyle', 'TBD') } / { data.get('strGenre', 'TBD') } ")
					st.write(f"** Country / Gender = ** { data.get('strCountry', 'TBD') } / { data.get('strGender', 'TBD') } ")
					st.write(f"** Artist Biography = ** { data.get('strBiographyEN', 'TBD') } ")
					st.write(f"** Artist Website = ** { data.get('strWebsite', 'TBD') } ")
					st.write(f"** Artist Twitter = ** { data.get('strTwitter', 'TBD') } ")
					st.write(f"** Artist Facebook = ** { data.get('strFacebook', 'TBD') } ")
					st.image(image = data.get('strArtistClearart', 'TBD'), width = 300)
				elif artist_name is not None and adb_category == 'Album':
					response_1: dict = requests.get(f'{BASE_URL}/searchalbum.php?s={artist_name.strip().lower()}').json()
					for data in response_1['album']:
						response_2: dict = requests.get(f"{BASE_URL}/track.php?m={data.get('idAlbum', 'TBD')}").json()
						with st.expander(label = f"Album Name = { data.get('strAlbum') }", expanded = False):
							st.image(image = data.get('strAlbumThumb', 'TBD'), width = 250)
							dataset: list = [{
								'Artist_Name': artist_name.title(), 'Album_ID': data.get('idAlbum', 'TBD'), 
								'Album_Name': data_2.get('strAlbum', 'TBD'), 'Year_Released': data.get('intYearReleased', 'TBD'),
								'Track_ID': data_2.get('idTrack', 'TBD'), 'Track_Name': data_2.get('strTrack', 'TBD'),
							} for data_2 in response_2['track']]
							st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
							st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Latest MP3 Songs':
			try:
				st.subheader('** Latest MP3 Songs **')
				BASE_URL: str = 'https://masstamilan.fm'
				Language: str = col_3.selectbox(label = 'Choose Language', options = ('Tamil', 'Hindi', 'Malayalam', 'Telugu'))
				st.write(f'** Selected Langauge = ** { Language } ')
				for i in range(1, 4):
					page_1 = soup(requests.get(f'{BASE_URL}/{Language.lower()}-songs?page={i}').text, 'lxml')
					for data_1 in page_1.find_all('div', class_= 'botitem'):
						movie_name: str = data_1.h1.text.strip()
						with st.expander(label = movie_name, expanded = False):
							st.write(f'** Movie Name = ** { movie_name } ')
							st.image(image = f"{ BASE_URL }{ data_1.img.get('src', '/TBD') }", width = 250)
							page_2 = soup(requests.get(f"{ BASE_URL }{ data_1.a.get('href', '/TBD') }").text, 'lxml')
							for data_2 in page_2.find_all('tr', {'itemprop': 'itemListElement'}):
								for data_3 in data_2.find_all('a', {'rel': 'nofollow'}):
									if data_3.get('title'):
										st.markdown(body = f'''
											<a href = "{ BASE_URL }{ data_3.get('href', '/TBD') }" target = '_blank'> { data_3.get('title') } </a> <br/>
											<audio controls> <source src = { BASE_URL }{ data_3.get('href', '/TBD') } type = 'audio/mp4'> </audio>
										''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'English Album Songs 1':
			try:
				st.subheader('** English Album Songs 1 **')
				Albums_List, BASE_URL, headers = [], 'https://nubeat.org', { 'User-Agent' : UserAgent().random }
				page_1 = soup(requests.get(url = f'{BASE_URL}/albums.html', headers = headers).text, 'lxml')
				for i in range(0, 4):
					temp_var: list = [ data for data in page_1.find_all('ul', class_ = 'icons')[i] ]
					Albums_List += [[temp_var[i].a.text, f"{BASE_URL}/{temp_var[i].a.get('href')}"] \
						for i in range(len(temp_var) - 1) if temp_var[i] != '\n']
				Album_Title: str = st.selectbox(label = 'Select English Song Album', options = [i for i,_ in Albums_List])
				for album_name, album_link in Albums_List:
					if Album_Title == album_name:
						st.write(f'** Album Name = { album_name } **')
						page_2 = soup(requests.get(url = album_link, headers = headers).text, 'lxml')
						titles: list = [data.text for data in page_2.find_all('a', class_='songtitle') if data.text != '']
						links: list = [f"{BASE_URL}/{data.get('src', 'TBD')}" for data in page_2.find_all('source')]
						for song_name, song_link in list(map(lambda x,y: [x,y], titles, links[0:int(len(links)/2)])):
							st.write(f'** Song Name = ** { song_name } ')
							st.markdown(body = f"<audio controls> <source src={ song_link } type='audio/mp4'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'English Album Songs 2':
			try:
				st.subheader('** English Album Songs 2 **')
				Album_Links, BASE_URL = [], 'https://songslover.vip'
				for i in range(1, 4):
					page_1 = soup(requests.get(f'{BASE_URL}/category/albums/page/{i}').text, 'lxml')
					Album_Links +=  [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('h2')[1:]]
				for album_name, album_link in Album_Links:
					with st.expander(label = f'Album Name = { album_name }', expanded = False):
						page_2 = soup(requests.get(url = album_link).text, 'lxml')
						st.image(image = page_2.find('figure').find('img').get('src'), width = 250)
						for data in page_2.find('ol').find_all('li'):
							st.write(f"** Song Name = ** { data.a.text } ")
							st.markdown(body = f"<audio controls> <source src = { data.a.get('href') } \
								type = 'audio/mp4'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')
				
		elif SUB_CATEGORY == 'English MP3 Songs':
			try:
				st.subheader('** English MP3 Songs 1 **')
				Song_Links, BASE_URL = [], 'https://songslover.vip'
				for i in range(1, 4):
					page_1 = soup(requests.get(url = f'{BASE_URL}/category/tracks/page/{i}').text, 'lxml')
					Song_Links += [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('h2')[1:]]
				for song_name, song_link in Song_Links:
					with st.expander(label = f'Song Name = { song_name }', expanded = False):
						page_2 = soup(requests.get(url = song_link).text, 'lxml')
						download_link = page_2.find_all('a', {'href': lambda x: x.endswith('.mp3')})[-1].get('href', 'TBD')
						st.write(f'** Song Name = ** { album_name } ')
						st.image(image = page_2.find('figure').find('img').get('src'), width = 250)
						st.markdown(body = f"<audio controls> <source src = { download_link } type = 'audio/mp4'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'English Video Songs':
			try:
				st.subheader('** English Video Songs **')
				Song_Links, BASE_URL = [], 'https://songslover.vip'
				for i in range(1, 3):
					page_1 = soup(requests.get(f'{BASE_URL}/category/download-video/page/{i}').text, 'lxml')
					Song_Links += [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('h2')[1:]]
				for song_name, song_link in Song_Links:
					page_2 = soup(requests.get( url = song_link ).text, 'lxml')
					download_link: str = page_2.find_all('a', {'href': lambda x: x.endswith('.mp4')})[-1].get('href')
					st.write(f'** Song Name = ** { song_name } ')
					st.markdown(body = f'''<video width = 320 height = 240 controls> <source src = { download_link } \
						type = 'video/mp4' autostart = 'false'> </video> ''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Hindi MP3 Songs':
			try:
				st.subheader('** Hindi MP3 Songs **')
				BASE_URL, Movie_Links, Year = 'https://mp3vista.com', [], datetime.now().year
				page_1 = soup(requests.get(url = f'{BASE_URL}/full-albums/').text, 'lxml')
				Movie_Links = [[data.a.text.strip(), data.a.get('href')] for data in \
					page_1.find_all('h3', class_ = 'entry-title') if Year in data.a.text.strip()]
				for movie_name, movie_link in Movie_Links[:10]:
					page_2 = soup(requests.get( url = movie_link ).text, 'lxml')
					st.write(f'** Movie Name = ** { movie_name } ')
					st.image(image = page_2.find_all('img')[1].get('data-lazy-src', 'TBD'), width = 250)
					movie: str = movie_name.replace('(','').replace(')','').replace(' ', '-')
					for data in page_2.find('div', class_='custom-field-album').find_all('p'):
						st.write(f"** Song Name = ** { data.a.text.strip() } ")
						st.markdown(body = f"""<a href = "https://cdn-mp3vista.live/full-albums/{movie}/{data.a.text.strip()} 320Kbps - Mp3Vista.Com.mp3" \
							target = '_blank'> Download Song (.MP3) </a>""", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Kannada MP3 Songs':
			try:
				st.subheader('** Kannada MP3 Songs **')
				page_1 = soup(requests.get(url = 'https://wsongs.com/').text, 'lxml')
				Movie_Links = [[data.text.strip(), data.a.get('href')] for data in page_1.find_all('li')]
				for movie_name, movie_link in Movie_Links:
					with st.expander(label = f'Movie Name = { movie_name }', expanded = False):
						page_2 = soup(requests.get(movie_link).text, 'lxml')
						for data in page_2.find_all('a', {'href': lambda x: x and x.endswith('.mp3')}):
							st.write(f'** Song Name = ** { data.text.strip() } ')
							st.markdown(body = f"<audio controls> <source src = { data.get('href') } \
								type = 'audio/mpeg'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Malayalam MP3 Songs':
			try:
				st.subheader('** Malayalam MP3 Songs **')
				Movie_Links, BASE_URL = [], 'https://kuttyweb.download'
				for i in range(1, 5):
					page_1 = soup(requests.get(f'{BASE_URL}/category/malayalam-songs/page/{i}/').text, 'lxml')
					Movie_Links += [[data.text.strip(), data.get('href')] for data in page_1.find_all('a', class_ = 'touch')]
				Movie_Title = st.selectbox(label = 'Select Malayalam Movie', options = [name for name,_ in Movie_Links])
				for movie_name, movie_link in Movie_Links:
					if Movie_Title == movie_name:
						st.write(f'** Movie Name = ** { movie_name } ')
						page_2 = soup(requests.get(url = movie_link).text, 'lxml')
						for data in page_2.find('div', class_='entry-content').find_all('p')[1:]:
							if data.a is not None:
								st.write(f'** Song Name = ** { data.text.strip() } ')
								st.markdown(body = f"<audio controls> <source src = { data.a.get('href') } \
									type = 'audio/mpeg'> </audio>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Online Radio 1':
			try:
				st.subheader('** Online Radio 1 **')
				col_1, col_2 = st.columns((2, 2))
				BASE_URL: str = random.choice(['https://de1.api.radio-browser.info', 'https://fr1.api.radio-browser.info', 
					'https://nl1.api.radio-browser.info'])
				response_1: dict = requests.get(url = f'{BASE_URL}/json/countries').json()
				countries: list = [ data.get('name', 'TBD') for data in response_1 if len(data['name']) < 20 ]
				country: str = col_1.selectbox(label = 'Select Country', options = countries )
				response_2: dict = requests.get(url = f'{BASE_URL}/json/stations/bycountry/{country}').json()
				languages: list = [ data.get('language', 'TBD') for data in response_2 if len(data['language']) > 1]
				lang_name: str = col_2.selectbox(label = 'Select Language', options = list(set(languages)) )
				for data in response_2:
					if data['language'] == lang_name:
						st.write(f"** Radio Name : ** {data.get('name', 'TBD')} ")
						st.write(f"** Country / Language : ** {data.get('country', 'TBD')} / {data.get('language', 'TBD')} ")
						st.audio(data = data.get('url', 'TBD'), format = 'audio/mpeg')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Online Radio 2':
			try:
				st.subheader('** Online Radio 2 **')
				filter_x: str = st.radio(label = 'Songs / Radio ?', options = ('Songs', 'Radio'))
				if filter_x == 'Songs':
					page = soup(requests.get('https://talk2trend.com/english-songs-mp3-download.html').text, 'lxml')
					for data in page.find('table').find_all('tr')[2:]:
						st.write(f"** Song Name = ** { data.find_all('td')[0].text.strip() } ")
						st.audio(data = data.find_all('td')[1].a.get('href', 'TBD'), format = 'audio/mpeg')
				elif filter_x == 'Radio':
					response: dict = requests.get(url = 'https://raw.githubusercontent.com/akashjeez/Study/master/radio_list.json').json()
					for data in response.get('Online_Radio'):
						st.write(f"** { data.get('Name') } **")
						st.audio(data = data.get('Link'), format = 'audio/mpeg')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Song Lyrics':
			try:
				st.subheader('** Song Lyrics **')
				col_1, col_2 = st.columns((2, 2))
				artist_name: str = col_1.text_input(label = 'Enter Artist Name', value = 'Eminem')
				song_name: str = col_2.text_input(label = 'Enter Song Name', value = 'Not afraid')
				if artist_name is not None and song_name is not None:
					artist_name, song_name = artist_name.title().strip(), song_name.title().strip()
					response: dict = requests.get(url = f'https://api.lyrics.ovh/v1/{artist_name}/{song_name}').json()
					st.write(f'** Artist : ** { artist_name } ** | Song Name : ** { song_name } ')
					for line in response['lyrics'].split('\n'):	st.write(line)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil God MP3 Songs':
			try:
				st.subheader('** Tamil God MP3 Songs **')
				song_links, BASE_URL = [], 'http://songtamil.in'
				page_1 = soup(requests.get(url = f'{BASE_URL}/mp3-songs/hindu-collections/').text, 'lxml')
				Album_Links = [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('div', class_='line')[:-3]]
				Album_Title: str = st.selectbox(label = 'Select Album', options = [name for name,_ in Album_Links] )
				for album_name, album_link in Album_Links:
					if album_name == Album_Title:
						st.write(f'** Album Name = ** { album_name } ')
						page_2 = soup(requests.get(url = album_link).text, 'lxml')
						for data in page_2.find_all('div', class_ = 'line'):
							if data.a is None:	continue
							if BASE_URL[15] in data.a.get('href'):
								page_3 = soup(requests.get( url = data.a.get('href') ).text, 'lxml')
								st.write('** Song Name = ** ', data.text.split('\n')[0].strip() )
								st.audio(data = page_3.find('a', {'rel': 'nofollow'}).get('href', 'TBD'), format = 'audio/mpeg')
			except Exception as ex:
				st.error(f'** Error : { ex } **')
		
		elif SUB_CATEGORY == 'Tamil MP3 Songs':
			try:
				st.subheader('** Tamil MP3 Songs **')
				Movie_Links, BASE_URL = [], 'http://starmusiq.top'
				for i in range(1, 5):
					page_1 = soup(requests.get(f'{BASE_URL}/home/page-{i}').text, 'lxml')
					Movie_Links += [[data.img.get('alt', 'TBD').replace('Download ', '').split(' Songs -')[0], data.img.get('src', 'TBD'), data.a.get('href', 'TBD')]
						for data in page_1.find('div', {'id': 'featured_albums'}).find_all('div', class_= 'img-thumbnail') if data.img is not None]
				Movie_Title: str = st.selectbox(label = 'Select Tamil Movie', options = [name for name,_,_ in Movie_Links])
				for movie_name, movie_poster, movie_link in Movie_Links:
					if movie_name == Movie_Title:
						st.write(f'** Movie Name = ** { movie_name } ')
						st.image(image = f'{BASE_URL}{movie_poster}', width = 300)
						page_2 = soup(requests.get(url = f'{BASE_URL}{movie_link}').text, 'lxml')
						for data in page_2.find('div', class_ = 'panel-body').find_all('a', {'class': 'text-info', 'target': '_blank'}):
							page_3 = soup(requests.get(f"{BASE_URL}{data.get('href')}").text, 'lxml')
							st.write(f'** Song Name = ** { data.text.strip() } ')
							st.audio(data = page_3.find('a', {'id': 'dBtn'}).get('href', 'TBD'), format = 'audio/mpeg')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Tamil Video Songs':
			try:
				st.subheader('** Tamil Video Songs **')
				Year, BASE_URL = datetime.now().year, 'http://tamilvideosda.net' 
				page_1 = soup(requests.get(url = f'{BASE_URL}/site_tamil_{Year}_videos_songs.xhtml').text, "lxml")
				Movie_Links: list = [[data.a.text.strip(), data.a.get('href')] for data in page_1.find_all('div', class_='f')]
				Movie_Title: str = st.selectbox(label = 'Select Tamil Movie', options = [name for name,_ in Movie_Links])
				for movie_name, movie_link in Movie_Links:
					if Movie_Title == movie_name:
						with st.expander(label = f'Movie Name = { movie_name }', expanded = False):
							page_2 = soup(requests.get(f'{BASE_URL}{movie_link}').text, "lxml")
							Movie_Songs = [[data.a.text.strip(), data.a.get('href')] for data in page_2.find_all('div', class_='f')]
							for song_name, song_link in Movie_Songs:
								page_3 = soup(requests.get(url = f'{BASE_URL}{song_link}').text, "lxml")
								if page_3.find('table') is None:	continue
								page_4 = soup(requests.get(page_3.find('td', class_='left').a.get('href')).text, 'lxml')
								download_link: str = page_4.find('a', {'rel': 'nofollow'}).get('href', 'TBD').replace(' ', '%20')
								st.write(f'** Song Name = ** { song_name } ')
								st.markdown(body = f'''<video width = 320 height = 240 controls> <source src = { download_link } \
									type = 'video/mp4' autostart = 'false'> </video> ''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

	
	elif CATEGORY == 'Sports':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Canada Football':
			try:
				st.subheader('** Canada Football **')
				BASE_URL, dataset = 'http://api.cfl.ca/v1/{}?key=T8Mv9BRDdcB7bMQUsQvHqtCGPewH5y8p', []
				filter_x: str = col_3.selectbox(label = 'Select Football Category', options = ('Teams', 
					'Standings', 'Games', 'Players') )
				if filter_x == 'Teams':
					response: dict = requests.get(url = BASE_URL.format('teams')).json()
					dataset: list = [{
						'Team_Code': data.get('abbreviation', 'TBD'), 'Team_Name': data.get('full_name', 'TBD'),
						'Venue_Name': data.get('venue_name', 'TBD'), 'Division': data.get('division_name', 'TBD'),
						'Team_Logo': data['images'].get('logo_image_url', 'TBD'),
					} for data in response['data'] ]
				elif filter_x == 'Standings':
					st.write('** P (Played), W (Win), L (Lost), T (Ties) **')
					response: dict = requests.get(url = BASE_URL.format(f'standings/{datetime.now().year}')).json()
					dataset: list = [{
						'Season': data.get('season', 'TBD'), 'Division_Name': data.get('division', 'TBD'),
						'Rank': data.get('place', 'TBD'), 'Team_Name': data.get('full_name', 'TBD'),
						'P-W-L-T': f"{ data.get('games_played', 'TBD') } - { data.get('wins', 'TBD') } - { data.get('losses', 'TBD') } - { data.get('ties', 'TBD') }", 
						'Points': data.get('points', 'TBD'), 'Winning%': data.get('winning_percentage', 'TBD'),
						'Points_For': data.get('points_for', 'TBD'), 'Points_Against': data.get('points_against', 'TBD'),
						'Home W-L-T': f"{ data.get('home_wins', 'TBD') } - { data.get('home_losses', 'TBD') } - { data.get('home_ties', 'TBD') }",
						'Away W-L-T': f"{ data.get('away_wins', 'TBD') } - { data.get('away_losses', 'TBD') } - { data.get('away_ties', 'TBD') }",
						'Division W-L-T': f"{ data.get('division_wins', 'TBD') } - { data.get('division_losses', 'TBD') } - { data.get('division_ties', 'TBD') }",
					} for division_name in ['west', 'east'] for data in response['data']['divisions'][division_name]['standings'] ]					
				elif filter_x == 'Games':
					response: dict = requests.get(url = BASE_URL.format(f'games/{datetime.now().year}')).json()
					for data in response['data']:
						data_dump: dict = {
							'Game_Date': data.get('date_start', 'TBD')[:10], 'Game_Number': data.get('game_number', 'TBD'),
							'Game_Week': data.get('week', 'TBD'), 'Game_Attendance': data.get('attendance', 'TBD'),
							'Game_Duration': data.get('game_duration', 'TBD'), 'Venue': data.get('venue', 'TBD'),
							'Ticket_URL': data.get('tickets_url', 'TBD'),
						}
						if coin_toss := data.get('coin_toss'):
							data_dump.update({ 'Coin_Toss_Winner': coin_toss.get('coin_toss_winner_election', 'TBD') })
						if weather := data.get('weather'):
							data_dump.update({
								'Teamperature': weather.get('temperature', 'TBD'), 'Sky': weather.get('sky', 'TBD'),
								'Wind_Speed': weather.get('wind_speed', 'TBD'), 'Wind_Duration': weather.get('wind_direction', 'TBD')
							})
						if team_1 := data.get('team_1'):
							if team_2 := data.get('team_2'):
								data_dump.update({
									'Team1_Name': team_1.get('nickename', 'TBD'), 'Team2_Name': team_2.get('nickname', 'TBD'),
									'Team1_Score': team_1.get('score', 'TBD'), 'Team2_Score': team_2.get('score', 'TBD'),
									'Winner': team_1.get('nickename', 'TBD') if team_1.get('score', 'TBD') > team_2.get('score', 'TBD') \
										else team_2.get('nickname', 'TBD')
								})
						dataset.append( data_dump )						
				elif filter_x == 'Players':
					response: dict = requests.get(url = BASE_URL.format('players')).json()
					dataset: list = [{
						'CFL_Central_ID': data.get('cfl_central_id', 'TBD'), 'DOB': data.get('birth_date', 'TBD'),
						'Player_Name': f"{ data.get('first_name', 'TBD') } { data.get('last_name', 'TBD') }",
						'Birth_Place': data.get('birth_place', 'TBD'), 'Height': data.get('height', 'TBD'),
						'Weight': data.get('weight', 'TBD'), 'Rookie_Year': data.get('rookie_year', 'TBD'),
						'School': data.get('school', 'TBD'), 'Position': data.get('position')
					} for data in response.get('data') ]
				st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
				st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Cricket Player Stats':
			try:
				st.subheader('** Cricket Player Stats **')
				BASE_URL, API_KEY = 'https://cricapi.com/api', 'vMmjfYwgk2P8Z9EIIm5CbkuBIYI2'
				player_name: str = st.text_input(label = 'Enter Cricket Player Name', value = 'dhoni')
				if player_name is not None and len( player_name ) > 0:
					response_1: dict = requests.get(f'{BASE_URL}/playerFinder?apikey={API_KEY}&name={player_name}').json()
					player_id: int = response_1['data'][0].get('pid', 123)
					response_2: dict = requests.get(f'{BASE_URL}/playerStats?apikey={API_KEY}&pid={player_id}').json()
					if 'imageURL' in response_2:	st.image(image = response_2.get('imageURL'))
					st.json( body = response_2 )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Sports Database':
			try:
				st.subheader('** Sports Database **')
				BASE_URL = 'https://thesportsdb.com/api/v1/json/1'
				response_1: dict = requests.get(url = f'{BASE_URL}/all_leagues.php').json()
				Leagues: list = [ league.get('strLeague', 'TBD') for league in response_1['leagues'] ]
				League: str = col_3.selectbox(label = 'Choose Sports League', options = Leagues )
				with st.expander(label = 'Teams', expanded = False):
					response_2: dict = requests.get(url = f'{BASE_URL}/search_all_teams.php?l={League}').json()
					dataset: list = [{
						'League_ID': data.get('idLeague', 'TBD'), 'League_Name': data.get('strLeague', 'TBD'),
						'Team_ID': data.get('idTeam', 'TBD'), 'Team_Name': data.get('strTeam', 'TBD'),
						'Country': data.get('strCountry', 'TBD'), 'Description': data.get('strDescriptionEN', 'TBD'), 
						'Team_Badge': data.get('strTeamBadge', 'TBD'), 'Team_Jersy': data.get('strTeamJersey', 'TBD'),
						'Team_Year_Founded': data.get('intFormedYear', 'TBD'), 
					} for data in response_2.get('teams') ]
					st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
					st.dataframe( data = pandas.DataFrame( data = dataset ) )
				with st.expander(label = 'Sports', expanded = False):
					response_2: dict = requests.get(url = f'{BASE_URL}/all_sports.php').json()
					for data in response_2.get('sports'):
						st.write(f"** Sport Name = ** { data.get('strSport', 'TBD') } ")
						st.image(image = data.get('strSportThumb', 'TBD'), width = 250)
						st.write(f"** Description = ** { data.get('strSportDescription', 'TBD') } ")
						st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Sport Stats':
			try:
				st.subheader('** Sport Stats **')
				sport_name: str = col_3.selectbox(label = 'Choose Sport', options =  ('FIFA', 'NBA', 'NFL', 
					'Tennis Men', 'Tennis Women', 'MotoGP Countries', 'MotoGP Riders', 'MLB') )
				if sport_name == 'FIFA':
					dataset = pandas.read_html('https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_records_and_statistics')[4]
				elif sport_name == 'NBA':
					dataset = pandas.read_html('https://basketball-reference.com/playoffs/')[0]
				elif sport_name == 'NFL':
					dataset = pandas.read_html('https://en.wikipedia.org/wiki/History_of_the_National_Football_League_championship')[2]
				elif sport_name == 'MLB':
					dataset = pandas.read_html('http://espn.com/mlb/worldseries/history/winners')[0]
				elif sport_name == 'Tennis Men':
					dataset = pandas.read_html('http://espn.com/tennis/history')[0]
				elif sport_name == 'Tennis Women':
					dataset = pandas.read_html('http://espn.com/tennis/history/_/type/women')[0]
				elif sport_name == 'MotoGP Countries':
					dataset = pandas.read_html('https://en.wikipedia.org/wiki/List_of_Grand_Prix_motorcycle_racing_World_champions')[2]
				elif sport_name == 'MotoGP Riders':
					dataset = pandas.read_html('https://en.wikipedia.org/wiki/List_of_Grand_Prix_motorcycle_racing_World_champions')[1]
				st.write(f'** Selected Sport = ** { sport_name } ')
				st.markdown( body = Excel_Downloader( pandas.DataFrame( data = dataset ) ), unsafe_allow_html = True)
				st.dataframe( data = pandas.DataFrame( data = dataset ) )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Sports News':
			try:
				st.subheader('** Sports News **')
				BASE_URL, headers = 'https://foxsports.com.au/content-feeds', { 'User-Agent': UserAgent().random }
				with st.expander(label = 'Live Cricket Score', expanded = False):
					page_1 = soup(requests.get(url = 'http://static.espncricinfo.com/rss/livescores.xml').text, 'lxml')
					for data in page_1.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.markdown(body = f"<a href = { data.guid.text } target = '_blank'> \
							More Details </a>", unsafe_allow_html = True)
				with st.expander(label = 'Sports News', expanded = False):
					page_2 = soup(requests.get(url = 'http://sportingnews.com/us/rss').text, 'lxml')
					for data in page_2.findAll('item'):
						st.write(f"** { data.description.text.replace(']]>','') } **")
						st.image(image = data.enclosure.get('url', 'TBD'), width = 250)
						st.write(f"** Published Date = ** { parse(data.pubdate.text).strftime('%d-%b-%Y %I:%M %p') } ")
						st.write(f'** Author = ** { data.author.text } ')
				with st.expander(label = 'Cricket', expanded = False):
					page_3 = soup(requests.get(url = f'{BASE_URL}/cricket/', headers = headers).text, 'lxml')
					for data in page_3.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.write( data.description.text.replace(']]>', '').strip() )
				with st.expander(label = 'NBA', expanded = False):
					page_4 = soup(requests.get(url = f'{BASE_URL}/nba/', headers = headers).text, 'lxml')
					for data in page_4.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.write( data.description.text.replace(']]>', '').strip() )
				with st.expander(label = 'WWE', expanded = False):
					page_5 = soup(requests.get(url = f'{BASE_URL}/wwe/', headers = headers).text, 'lxml')
					for data in page_5.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.write( data.description.text.replace(']]>', '').strip() )
				with st.expander(label = 'NFL', expanded = False):
					page_6 = soup(requests.get(url = f'{BASE_URL}/nfl/', headers = headers).text, 'lxml')
					for data in page_6.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.write( data.description.text.replace(']]>', '').strip() )
				with st.expander(label = 'Tennis', expanded = False):
					page_7 = soup(requests.get(url = f'{BASE_URL}/tennis/', headers = headers).text, 'lxml')
					for data in page_7.findAll('item'):
						st.write(f'** { data.title.text.strip() } **')
						st.write( data.description.text.replace(']]>', '').strip() )
			except Exception as ex:
				st.error(f'** Error : { ex } **')


	elif CATEGORY == 'Useful':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Bitcoin Price':
			try:
				st.subheader('** Live Bitcoin Market Price **')
				col_1, col_2 = st.columns((2, 2))
				start_date: str = col_1.date_input('Start Date', (datetime.now() - timedelta(days = 30)) )
				end_date: str = col_2.date_input('End Date', datetime.now() )
				timespan: str = f'{ (end_date - start_date).days }days'
				st.write(f'** Your Input = {timespan} **')
				dataset = pandas.DataFrame( data = Bitcoin_Price( timespan = timespan ) )
				dataset['Date'] = pandas.to_datetime(dataset.Date)
				dataset.set_index('Date', inplace = True)
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				with st.expander(label = 'Show Raw Data!', expanded = False):
					st.dataframe( data = dataset )
				st.write('** The average USD Market Price Across Major Bitcoin Exchanges. **')
				st.line_chart( data = dataset.Value )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Age Calculator':
			try:
				st.subheader('** Age Calculator **')
				input_date: str = st.date_input(label = 'Your Date-of-Birth', value = (datetime.today() - timedelta(days = 36500)) )
				age_calc: float = round( ( ( datetime.now().date() - input_date ).days / 365 ), 2)
				st.write(f"** Your Age is { age_calc } ** ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Google Translator':
			try:
				st.subheader('** Google Translator **')
				col_1, col_2 = st.columns((2, 2))
				keyword: str = col_1.text_input(label = 'Enter Keyword', value = '')
				language: str = col_2.selectbox(label = 'Choose Language', options = list(LANGUAGES.keys()) )
				if len( keyword ) > 0 and language is not None:
					translator = Translator(service_urls = ['translate.google.com'])
					result = translator.translate( text = keyword.strip(), dest = LANGUAGES[language] )
					st.write(f' ** Input keyword = ** { keyword }')
					st.write(f' ** Input Language = ** { language }')
					st.write(f' ** Result = ** { result.text }')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Stock Ticker':
			try:
				st.subheader('** Stock Ticker **')
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				df = pandas.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
				df.rename(columns = {'Symbol': 'symbol', 'Security': 'company_name', 'GICS Sector': 'industry'}, inplace = True)
				companies = df[['company_name', 'symbol', 'industry']]
				input_company: str = col_3.selectbox(label = 'Choose Company Name', options = list(set(companies.company_name.unique())) )
				company_code = companies[ companies.company_name == input_company ].symbol.values.tolist()[0].strip()
				st.write(f' ** Company Name = ** { input_company.title() } ** | Code = ** { company_code } ')
				start_date: str = col_1.date_input('Enter Start Date', (datetime.today() - timedelta(days = 30)) )
				end_date: str = col_2.date_input('Enter End Date', datetime.today() )
				dataset = yf.download(tickers = company_code.upper(), start = start_date, end = end_date, progress = False)
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
				parameters: list = st.multiselect(label = 'Select Parameters', options = list(dataset.columns), default = ['Close'] )
				st.line_chart( data = dataset[parameters] if len(parameters) > 0 else dataset['Close'] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Google Map Search':
			try:
				st.subheader('** Google Map Search **')
				location: str = st.text_input(label = 'Enter Location Name', value = 'Chennai')
				if location is not None:
					URL = f'https://google.com/maps/embed/v1/place?q={location}&key=AIzaSyAMAkoV7402tDGkBtP36pfGb4BFqXtq9QI'
					st.markdown( body = f'<iframe width = 600 height = 450 frameborder = 0 style=border:0 \
						src = { URL } allowfullscreen> </iframe>', unsafe_allow_html = True )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Currency Exchange':
			try:
				st.subheader('** Currency Exchange **')
				dataset: dict = requests.get(url = 'https://api.exchangeratesapi.io/latest?base=USD').json()
				st.write(f'** Base is USD (United States Dollar) ** ')
				st.json( data = dataset.get('rates', 'TBD') )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Love Calculator':
			try:
				st.subheader('** Love Calculator **')
				boy_name, girl_name = st.text_input('Enter Boy Name'), st.text_input('Enter Girl Name')
				if boy_name is not None and girl_name is not None:
					score: int = 100 - (len(boy_name.replace(' ','')) * len(girl_name.replace(' ',''))) - (random.randint(1,3))
					st.write(f'** Love Between { boy_name } and { girl_name } is ** { score } %')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Urban Dictionary':
			try:
				st.subheader('** Urban Dictionary **')
				keyword: str = st.text_input(label = 'Enter Keyword', value = '')
				if keyword is not None and len( keyword ) > 0:
					keyword: str = keyword.replace(' ','+').lower()
					response: dict = requests.get(f'https://api.urbandictionary.com/v0/define?term={keyword}').json()
					for data in response['list']:
						st.write(f"** Word : ** {data.get('word', 'TBD')}")
						st.write(f"** Definition : ** {data.get('definition')}")
						st.write(f"** Example : ** {data.get('example', 'TBD')}")
						st.write(f"** Thumps Up : ** {data.get('thumbs_up', 'TBD')}")
						st.write(f"** Thumps Down : ** {data.get('thumbs_down', 'TBD')}")
						st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Best Poetries':
			try:
				st.subheader('** Best Poetries **')
				response_1 = requests.get('http://poetrydb.org/author').json()
				author: str = st.selectbox(label = 'Choose Author', options = response_1['authors'] )
				response: dict = requests.get(f'http://poetrydb.org/author/{author}/author,title,lines,linecount')
				for data in response.json():
					with st.expander(label = f"Title = { data.get('title', 'TBD') } ", expanded = False):
						st.write(f"** Title : ** { data.get('title', 'TBD') } ")
						st.write(f"** Author : ** { data.get('author', 'TBD') } ")
						st.write(f"** Poet : **")
						for line in data['lines']:	st.write(line)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Youtube Downloader':
			try:
				st.subheader('** YouTube Audio / Video Downloader **')
				youtube_link: str = st.text_input(label = 'Paste your YouTube Video URL', value = '')
				if youtube_link is not None and len( youtube_link ) > 0:
					video_id: str = youtube_link.split('=')[-1] if '/watch' in youtube_link else youtube_link.split('/')[-1]
					dataset: dict = YouTube_Downloader( video_id = video_id )
					with st.expander(label = 'Video Details', expanded = False):
						st.write(f"** Video Title : ** { dataset.get('Title', 'TBD') } ")
						st.write(f"** Video Rating : ** { dataset.get('Rating', 'TBD') } ")
						st.write(f"** Video View Count : ** { dataset.get('ViewCount', 'TBD') } ")
						st.write(f"** Video Author : ** { dataset.get('Author', 'TBD') } ")
						st.write(f"** Video Length : ** { dataset.get('Length', 'TBD') } ")
						st.write(f"** Video Duration : ** { dataset.get('Duration', 'TBD') } ")
						st.write(f"** Video Category : ** { dataset.get('Category', 'TBD') } ")
						st.write(f"** Video Likes : ** { dataset.get('Likes', 'TBD') } ")
						st.write(f"** Video DisLikes : ** { dataset.get('Dislikes', 'TBD') } ")
					with st.expander(label = 'Play YouTube Video', expanded = False):
						Play_YTVideo: str = f'https://youtube.com/embed/{ video_id }'
						st.markdown(body = f"<iframe width = 400 height = 350 src = '{ Play_YTVideo }' frameborder = 0 allow = 'accelerometer; \
							autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen> </iframe>", unsafe_allow_html = True)
					with st.expander(label = 'Download Videos', expanded = False):
						for video in dataset.get('videos'):
							st.write(f"** Resolution : {video.get('Resolution', 'TBD')} | Extension : {video.get('Extension', 'TBD')} | Size: {video.get('FileSize', 'TBD')} **")
							st.markdown(body = f"<a href = '{video.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Video >> </a>", unsafe_allow_html = True)
					with st.expander(label = 'Download Audios', expanded = False):
						for audio in dataset.get('audios'):
							st.write(f"** Extension : {audio.get('Extension', 'TBD')} | Size: {audio.get('FileSize', 'TBD')} **")
							st.markdown(body = f"<a href = '{audio.get('DownloadLink', 'TBD')}' target = '_blank'> << Download Audio >> </a>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Coronavirus Stats':
			try:
				st.subheader('** CoronaVirus Stats **')
				col_1, col_2, col_3, col_4 = st.columns((2, 2, 2, 2))
				filter_x: str = col_4.selectbox(label = 'Advanced Filter', options = ('Overiew Stats', 'Detailed Stats', 'Country India'))
				if filter_x == 'Overiew Stats':
					data_dump = Coronavirus_Dataset()
					categories: str = col_1.selectbox(label = 'Continents / Countries?', options = ['Continents', 'Countries'] )
					start_date: str = col_2.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 30)) )
					end_date: str = col_3.date_input(label = 'End Date', value = datetime.now() )
					start_date, end_date = str(start_date), str(end_date)
					if categories == 'Countries':
						locations: list = st.multiselect(label = 'Select Countries', default = ['India', 'United States'], 
							options = [country for country in data_dump.location.unique()] )
						st.write(f"** > Selected Countries are ** {', '.join( locations )} ")
						data_dump_1 = data_dump[ (data_dump.location.isin( locations )) ]
					else:
						continents: list = st.multiselect(label = 'Select Continents', default = ['Asia'], 
							options = [country for country in data_dump.continent.unique()] )
						st.write(f"** > Selected Continents are ** {', '.join( continents )} ")
						data_dump_1 = data_dump[ (data_dump.continent.isin( continents )) ]
					dataset = data_dump_1[ (data_dump_1.date >= start_date) & (data_dump_1.date <= end_date) ]
					st.write(f'** > Selected Date Range From ** { start_date } TO { end_date } ')
					st.write(f'** Stats = ** Cases : { int(dataset.new_cases.sum()) } | Deaths : { int(dataset.new_deaths.sum()) } ')
					st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
					chart_data = dataset[['date', 'new_cases', 'new_deaths', 'total_cases', 'total_deaths']]
					chart_data.set_index('date', inplace = True)
					parameters = st.multiselect(label = 'Select Parameters', options = list(chart_data.columns), default = ['total_cases'], )
					st.line_chart( data = chart_data[parameters] if len(parameters) > 0 else chart_data['total_cases'] )
				elif filter_x == 'Detailed Stats':
					data_dump = pandas.DataFrame( requests.get('https://trackcorona.live/api/countries').json()['data'] )
					locations: list = st.multiselect(label = 'Select Countries', default = ['India', 'United States'],
						options = [country for country in data_dump.location.unique()] )
					st.write(f"** > Selected Countries are ** {', '.join(locations)} ")
					dataset = data_dump if len(locations) == 0 else data_dump[ (data_dump.location.isin( locations )) ]
					st.write('** Stats = ** Total Cases : {} | Total Deaths : {} | Total Recovered : {} '.format(
						int(dataset.confirmed.sum()), int(dataset.dead.sum()), int(dataset.recovered.sum()) ))
					st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
					## Show DataFrame & Map
					st.dataframe( data = dataset )
					st.map( data = dataset, zoom = 2)
				elif filter_x == 'Country India':
					dataset = Coronavirus_Dataset_India()
					st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
					st.write("** Stats = ** Total Cases : {} | Total Recovered : {} | Total Deaths : {}".\
						format( int(dataset.Confirmed.sum()), int(dataset.Recovered.sum()), int(dataset.Deaths.sum()) ))
					st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Verify Phone Number':
			try:
				st.subheader('** Verify Phone Number **')
				BASE_URL, API_KEY = 'http://apilayer.net/api', '60a8f024d2fbe01e95d1f474992b0598'
				phone_num: str = st.text_input(label = 'Enter Mobile Number without +91 ', value = '')
				if phone_num is not None and len( phone_num ) > 0:
					response = requests.get(url = f'{BASE_URL}/validate?access_key={API_KEY}&number={phone_num}&country_code=IN').json()
					if 'valid' in response.keys() and response['valid'] == True:
						st.write(f" ** Mobile Number = ** { response.get('international_format', 'TBD') } ")
						st.write(f" ** SIM Card Carrier = ** { response.get('carrier', 'TBD') } ")
						st.write(f" ** Location = ** { response.get('location', 'TBD') } ")
						st.write(f" ** Country = ** { response.get('country_name', 'TBD') } ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Job Portal':
			try:
				st.subheader('** Job Portal **')
				keyword: str = st.text_input(label = 'Enter Keyword', value = 'Python')
				if keyword is not None and len( keyword ) > 0:
					response = requests.get(url = f"https://jobs.github.com/positions.json?title={keyword.lower()}")
					for data in response.json():
						st.markdown( data = f"<img class = 'rounded-circle article-img' src='{data.get('company_logo', 'TBD')}' \
							width = 200 height = 200>", unsafe_allow_html = True )
						st.write(f"** Job Title : ** {data.get('title', 'TBD')} ")
						st.write(f"** Job Location : ** {data.get('location', 'TBD')} ")
						st.write(f"** Job Company : ** {data.get('company', 'TBD')} ")
						st.markdown( data = f"** <a href = '{data.get('company_url', 'TBD')}' target = '_blank'> << Company URL>> </a> |\
							<a href = '{data.get('url', 'TBD')}' target = '_blank'> << Apply URL>> </a> **", unsafe_allow_html = True)
						st.write(f"** Job Type : ** {data.get('type', 'TBD')} ")
						st.write(f"** Job Posted Date : ** {data.get('created_at', 'TBD')} ")
						st.write(f"** Job Description : ** {data.get('description', 'TBD')} ")
						st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Proxy List':
			try:
				st.subheader('** Proxy List **')
				st.write('''A proxy list is a list of open HTTP/HTTPS/SOCKS proxy servers all on one website. 
					Proxies allow users to make indirect network connections to other computer network services.''')
				dataset: dict = Proxy_List_Dataset( ['https://sslproxies.org/', 'https://free-proxy-list.net/'] )
				param_1: str = st.selectbox(label = 'Choose Parameter', options = ['ALL', 'Country', 'Anonymity', 'Https'] )
				if param_1 == 'ALL':
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
				else:
					sub_params = [data for data in dataset[param_1].unique()]
					param_2 = st.multiselect(label = f'Select { param_1 }', options = sub_params, default = sub_params)
					if param_2 is not None:
						st.markdown( body = Excel_Downloader( dataset[ dataset[param_1].isin(param_2) ] ), unsafe_allow_html = True)
						st.dataframe( data = dataset[ dataset[param_1].isin(param_2) ] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Live News':
			try:
				st.subheader('** Live News **')
				st.write(' Get Breaking News Headlines and Search for Articles From Worldwide News Sources and Blogs All Over the Web. ')
				BASE_URL, API_KEY = 'http://newsapi.org/v2', '4dbc17e007ab436fb66416009dfb59a8'
				keyword: str = st.text_input(label = 'Enter Keyword', value = 'education')
				if keyword is not None and len( keyword ) > 0:
					response = requests.get(url = f"{BASE_URL}/everything?q={keyword.lower()}&apiKey={API_KEY}")
					for data in response.json()['articles']:
						st.markdown( f"<img class = 'rounded-circle article-img' src='{data.get('urlToImage', 'TBD')}' \
							width = 200 height = 200>", unsafe_allow_html = True )
						st.write(f"** { data.get('title', 'TBD') } **")
						st.write(f"** Description : ** { data.get('description', 'TBD') } ")
						st.write(f"** Content : ** { data.get('content', 'TBD') } ")
						st.write(f"** Author : ** { data.get('author', 'TBD') } ")
						st.write(f"** Published Date : ** { parse( data.get('publishedAt')).strftime('%d-%b-%Y %I:%M %p') } ")
						st.write(f"** For More Details, Please Click { data.get('url','TBD') } ** ")
						st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Cloud Market Cost':
			try:
				st.subheader('** Cloud Market Cost **')
				col_1, col_2, col_3, col_4, col_5 = st.columns((2, 2, 2, 2, 2))
				providers: dict = {'Alibaba': 'alibaba', 'Amazon AWS': 'amazon', 'Google GCP': 'google', 'Microsoft Azure': 'azure'}
				provider: str = col_3.selectbox(label = 'Choose Cloud Provider', options = list(providers.keys()) )
				dataset: dict = Cloud_Cost_Dataset( provider = providers.get(provider) )
				adv_filter: str = col_1.selectbox(label = 'Advanced Filter ?', options = ['Yes', 'No'])
				if adv_filter == 'No':
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
				else:
					input_cpu: str = col_2.selectbox(label = 'Choose CPU', options = list(range(1, 201)) )
					input_memory: str = col_4.selectbox(label = 'Choose RAM Memory ', options = list(range(1, 1001)) )
					input_region: str = col_5.selectbox(label = 'Choose Region', options = [data for data in dataset.region_name.unique()])
					if input_cpu and input_memory and input_region:
						data_dump = dataset[ (dataset.cpu <= int(input_cpu)) & (dataset.memory <= float(input_memory)) & \
							(dataset.region_name == input_region) ]
						st.markdown( body = Excel_Downloader( data_dump ), unsafe_allow_html = True)
						st.dataframe( data = data_dump )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Temperature':
			try:
				st.subheader('** Temperature Conversion **')
				st.text(' Normal : 36.5 – 37.5 °C (97.7 – 99.5 °F) ')
				st.text(' Fever : > 37.5 - 38.3 °C (99.5 - 100.9 °F) ')
				st.text(' Hypothermia : < 35.0 °C (95.0 °F) ')
				input_degree: float = st.number_input(label = 'Enter Temperature Degree', min_value = 0.0, value = 0.01, step = 0.01)
				if input_degree is not None and len( input_degree ) > 0:
					conversion_type: str = st.selectbox(label = 'Choose Temperature Conversion Type', 
						options = ['Celsius to Fahrenheit', 'Fahrenheit to Celsius'] )
					if conversion_type == 'Celsius to Fahrenheit':
						result: float = round(input_degree * 9 / 5 + 32, 2)
						st.write(f"** { input_degree } Degree Celsius is equal to { result } Degree Fahrenheit. **")
					else:
						result: float = round( (input_degree - 32) * 5 / 9, 2)
						st.write(f"** { input_degree } Degree Fahrenheit is equal to { result } Degree Celsius. **")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Social Media Stats':
			try:
				st.subheader('** Social Media Stats **')
				BASE_URL, year = 'https://kworb.net', datetime.now().year
				st.write('** Most Liked Videos **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/topvideos_likes.html')[0] )
				st.write('**  Most Disliked Videos **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/topvideos_dislikes.html')[0] )
				st.write('**  Most Commented Videos **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/topvideos_comments.html')[0] )
				st.write('**  Most Viewed Videos in 24 Hours **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/realtime_anglo.html')[0] )
				st.write(f'** Most Viewed in Year {year} **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/topvideos2019.html')[0] )
				st.write(f'** Top Artist in Year {year} **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/topartists_{year}.html')[0] )
				st.write('** Trending Videos **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/youtube/trending.html')[0] )
				st.write('** Spotify Charts **')
				st.dataframe( data = pandas.read_html(f'{BASE_URL}/spotify/country/global_daily.html')[0] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Bank IFSC Code':
			try:
				st.subheader('** Bank IFSC Code **')
				col_1, col_2 = st.columns((2, 2))
				bank_list: list = requests.get(url = 'https://api.techm.co.in/api/listbanks').json()['data']
				bank_name: str = col_1.selectbox(label = 'Select Bank', options = bank_list)
				branches: dict = requests.get(f'https://api.techm.co.in/api/listbranches/{bank_name}', timeout = 6000).json()
				branch_name: str = col_2.selectbox('Select Branch', branches['data'])
				details: dict = requests.get(f'https://api.techm.co.in/api/getbank/{bank_name}/{branch_name}', timeout = 6000).json()
				if details := details.get('data'):
					st.write(f"** BANK NAME : ** { details.get('BANK', 'TBD') } ")
					st.write(f"** BRANCH NAME : ** { details.get('BRANCH', 'TBD') } ")
					st.write(f"** IFSC CODE : ** { details.get('IFSC', 'TBD') } ")
					st.write(f"** MICR CODE : ** { details.get('MICRCODE', 'TBD') } ")
					st.write(f"** ADDRESS : ** { details.get('ADDRESS', 'TBD') } ")
					st.write(f"** STATE NAME : ** { details.get('STATE', 'TBD') } ")
					st.write(f"** CITY NAME : ** { details.get('CITY', 'TBD') } ")
					st.write(f"** DISTRICT NAME: ** { details.get('DISTRICT', 'TBD') } ")
					st.write(f"** CONTACT : ** { details.get('CONTACT', 'TBD') } ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Instagram BOT':
			try:
				st.subheader('** Instagram BOT **')
				## Load the DataSet with Streamlit Cache.
				username: str = st.text_input(label = 'Enter Instagram UserName ', value = 'akashjeez')
				if username is not None and len( username ) > 0:
					dataset: dict = Instagram_Bot(insta_url = f'https://instagram.com/{username.lower()}')
					st.markdown( f"<img class = 'rounded-circle article-img' src='{dataset.get('profile_pic_hd', 'TBD')}'\
						width = 200 height = 200>", unsafe_allow_html = True )
					st.json( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Docker Rest API':
			try:
				st.subheader('** Docker Rest API **')
				BASE_URL, col_1, col_2 = 'https://hub.docker.com/v2', st.columns((2, 2))
				category: str = col_1.selectbox(label = 'Basics / Advanced Search', options = ['Basics', 'Advanced'])
				if category == 'Basics':
					data_dump = list( 
						chain.from_iterable( [requests.get(f'{BASE_URL}/repositories/library/?page={i}&page_size=100').json()['results'] for i in range(1, 3)] ) 
					)
					image_names: list = [f"{ data['namespace'] }/{ data['name'] }" for data in data_dump]
					image_name: str = col_2.selectbox(label = 'Select Docker Image Name', options = image_names )
					dataset = Docker_Rest_API( image_name = image_name.lower() )
					st.json( data = dataset )
				else:
					username: str = col_2.text_input(label = 'Enter Docker Username', value = 'akashjeez')
					user_details: dict = requests.get(url = f'{BASE_URL}/users/{username.lower()}?page_size=100').json()
					user_image_url: str = user_details.get('gravatar_url', 'TBD').replace('s=80', 's=120')
					st.markdown( f"<img class = 'rounded-circle article-img' src = {user_image_url} width = 200 height = 200>", 
						unsafe_allow_html = True )
					st.write('\n Docker Account User Details : ')
					st.json( data = user_details )
					response: dict = requests.get(url = f'{BASE_URL}/repositories/{username.lower()}?page_size=100').json()
					st.write('\n Docker Repository Image Details & Tags : ')
					for data in response['results']:
						st.json( data = Docker_Rest_API( image_name = f"{ data['user'] }/{ data['name'] }".lower() ) )
						st.write( '*' * 50 )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Forbes Billionaires':
			try:
				st.subheader('** Forbes Billionaires **')
				st.write('''The World's Billionaires is an Annual Ranking by Documented Net Worth of the Wealthiest 
					Billionaires in the World, and Published in March Annually by the American Business Magazine Forbes.''')
				json_response, dataset = Forbes_Billionaires()
				countries: list = col_3.multiselect(label = 'Choose Countries', options = list(set(dataset.Country)),
					default = ['United States', 'Russia'] )
				dataset = dataset[ dataset.Country.isin(countries) ]
				st.markdown( body = Excel_Downloader(dataset), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Open Trivia':
			try:
				st.subheader('** Open Trivia **')
				col_1, col_2 = st.columns((2, 2))
				limit: int = col_1.slider(label = 'How Many Questions ?', min_value = 1, max_value = 50, value = 10, step = 1)
				difficulty: str = col_2.selectbox(label = 'Choose Difficulty', options = ['Easy', 'Medium', 'Hard'] )
				for data in Open_Trivia( limit, difficulty.lower() ):
					st.write('** Category ** : ', data.get('category', 'TBD') )
					st.write('** Difficulty ** : ', data.get('difficulty', 'TBD').title() )
					st.write('** Question ** : ', data.get('question', 'TBD') ),
					st.write('** Correct Answer ** : ', data.get('correct_answer', 'TBD') )
					st.write('** InCorrent Answers ** : ', data.get('incorrect_answers', 'TBD') )
					st.write('*' * 50)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Weather Report':
			try:
				st.subheader('** Weather Report **')
				city_name: str = st.text_input(label = 'Enter City Name (NOT Country Name)', value = 'Chennai')
				BASE_URL: str = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}'
				response: dict = requests.get( url = BASE_URL.format(city_name.lower(), '28a31767a1909138a53410a56233a326') ).json()
				st.markdown(f"<img src = 'http://openweathermap.org/img/wn/{response['weather'][0]['icon']}.png' />", unsafe_allow_html = True)
				st.write('** City Name ** : ', response.get('name', 'TBD') )
				st.write(f"** Coordinates - Latitude {response['coord']['lat']} & Longitude {response['coord']['lon']} **")
				st.write('** Description ** : ', response['weather'][0]['description'] )
				st.write(f"** Temperature ** : {response['main']['temp']} F ")
				st.write('** Humidity ** : ', response['main']['humidity'] )
				st.write('** Wind Speed ** : ', response['wind']['speed'] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Python Tutorial':
			try:
				st.subheader('** Python Tutorial **')
				st.write('Python is a Programming Language That Lets You Work Quickly and Integrate Systems More Effectively.')
				online_compiler_link: str = 'https://console.python.org/python-dot-org-console/'
				st.markdown(body = "<a href = 'https://twitter.com/ThePSF?ref_src=twsrc%5Etfw' target='_blank'> Follow @ThePSF </a>", unsafe_allow_html = True)
				with st.expander(label = 'Python Online Compiler', expanded = False):
					st.markdown(body = f"<iframe src = '{online_compiler_link}' width = 700 height = 300 frameborder = 0> </iframe>", unsafe_allow_html = True)
				with st.expander(label = 'Online Python Learning', expanded = False):
					st.markdown(body = f"<a href = 'https://w3schools.com/python/' target = '_blank'> << W3Schools >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://pythonprogramming.net/' target = '_blank'> << PythonProgramming.Net >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://programiz.com/python-programming' target = '_blank'> << ProgramiZ >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://datacamp.com/' target = '_blank'> << DataCamp >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://awesome-python.com/' target = '_blank'> << Awesome Python >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://realpython.com/' target = '_blank'> << Real Python >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://guide.freecodecamp.org/python/' target = '_blank'> << Free-Code-Camp >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://sololearn.com/Course/Python/' target = '_blank'> << SoloLearn >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://web.programminghub.io/' target = '_blank'> << Programming Hub >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://youtu.be/_uQrJ0TkZlc' target = '_blank'> << Youtube - Python Absolute for Beginners >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://data36.com/' target = '_blank'> << Python Data Science for Beginners >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://tutorialsteacher.com/python' target = '_blank'> << Tutorials Teacher >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://morioh.com' target = '_blank'> << Morioh >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://tutorialedge.net/course/python/' target = '_blank'> << Tutorials Edge >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://listendata.com/search/label/Python' target = '_blank'> << Listen Data >> </a>", unsafe_allow_html = True)
					st.markdown(body = f"<a href = 'https://data-flair.training/blogs/python-tutorial/' target = '_blank'> << Data Flair >> </a>", unsafe_allow_html = True)
				with st.expander(label = 'Python Package / Module Search', expanded = False):
					st.write('** Python Package / Module Search **')
					dataset, BASE_URL = [], 'https://pypi.org'
					tree = html.fromstring(requests.get(f'{BASE_URL}/simple').content)
					input_package: str = st.text_input(label = 'Enter Python Package Name', value = 'pandas')
					for package in tree.xpath('//a/text()'):
						if input_package.lower() == package:
							response: dict = requests.get(f'{BASE_URL}/pypi/{package}/json/').json()
							data_info, data_urls = response['info'], response['urls']
							dataset.append({
								'package_name': package.title(), 'package_url': data_info.get('package_url', 'TBD'),
								'author': data_info.get('author', 'TBD'), 'author_email': data_info.get('author_email', 'TBD'),
								'home_page': data_info.get('home_page', 'TBD'), 'project_url': data_info.get('project_url', 'TBD'),
								'release_url': data_info.get('release_url', 'TBD'), 'summary': data_info.get('summary', 'TBD'),
								'requires_python': data_info.get('requires_python', 'TBD'), 'version': data_info.get('version', 'TBD'),
								'urls': [{
									'filename': url.get('filename', 'TBD'), 'download_url': url.get('url',' TBD'),
									'last_uploaded': datetime.strptime(url['upload_time'], '%Y-%m-%dT%H:%M:%S').strftime('%d-%b-%Y %I:%M %p')
								} for url in data_urls], 'classifiers': data_info.get('classifiers', 'TBD'),
							})
					st.json( data = {'count': len(dataset), 'data': dataset} )
				st.write('*' * 50)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Microsoft Learn':
			try:
				st.subheader('** Microsoft Learn **')
				col_1, col_2 = st.columns((2, 2))
				st.write('The Microsoft Learn Catalog API Lets You Send a Web-Based Query to Microsoft Learn and \
					Get Back Details About Published Content Such as Titles, Products Covered, and Links to the Training.')
				response: dict = requests.get('https://docs.microsoft.com/api/learn/catalog').json()
				section: str = col_1.selectbox(label = 'Select Section', options = list(response.keys()) )
				view_format: str = col_2.selectbox(label = 'Data Table / JSON Format ?', options = ('Data Table', 'JSON') )
				if view_format == 'Data Table':
					dataset = pandas.DataFrame( data = response[ section ] )
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
				elif view_format == 'JSON':
					st.json( data = response[ section ] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Indian Railways':
			try:
				st.subheader('** Indian Railways **')
				col_1, col_2, col_3, col_4 = st.columns((2, 2, 2, 2))
				BASE_URL, API_KEY = 'https://indianrailapi.com/api/v2', '0d09f3ec0a9dd22dd42bbf13c697c289'
				collections: tuple = ('Ticket Cost', 'Trains on Station', 'Station Search')
				collection: str = col_3.selectbox(label = 'Choose Category', options = collections )
				if collection == 'Ticket Cost':
					train_num: int = col_1.text_input(label = 'Enter Train Number', value = '')
					source_station_code: str = col_2.text_input(label = 'Enter Source Station Code').upper()
					dest_station_code: str = col_4.text_input(label = 'Enter Destination Station Code').upper()
					if train_num and source_station_code and dest_station_code:
						queries: str = f'TrainNumber/{train_num}/From/{source_station_code}/To/{dest_station_code}/Quota/GN'
						response: dict = requests.get(body = f'{BASE_URL}/TrainFare/apikey/{API_KEY}/{queries}').json()
						st.json( data = response )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Emojis Search':
			try:
				st.subheader('** Emojis Search **')
				col_1, col_2 = st.columns((2, 2))
				choice: str = col_1.selectbox(label = 'Search by Category / Tag Name ?', options = ('Category', 'Tag') )
				if choice == 'Category':
					categories = col_2.multiselect(label = 'Select Emoji Categories', options = list(emojis.db.get_categories()), 
						default = list(emojis.db.get_categories())[-3 : -1] )
					dataset = [{
						'emoji_name': data.aliases[0], 'emoji': data.emoji, 'emoji_tags': data.tags, 'category': data.category
					} for category in categories for data in emojis.db.get_emojis_by_category( category ) ]
				else:
					tags = col_2.multiselect(label = 'Select Emoji Tags', options = list(emojis.db.get_tags()), 
						default = list(emojis.db.get_tags())[-3 : -1] )
					dataset = [{
						'emoji_name': data.aliases[0], 'emoji': data.emoji, 'emoji_tags': data.tags, 'category': data.category
					} for tag in tags for data in emojis.db.get_emojis_by_tag( tag ) ]
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Text Analysis':
			try:
				st.subheader('** Text Analysis **')
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				sentence: str = col_3.text_input(label = 'Type Sentence', value = '')
				if sentence is not None and len( sentence ) > 0:
					blob = TextBlob( sentence.strip().title() )
					lang_reverse: dict = { value: key for key, value in languages.items() }
					choice: str = col_1.radio(label = 'Choose Type', options = ('Language Detection', 'Language Translation', 
						'Synonyms Antonyms', 'Spelling Correction', 'Sentiment Analysis',) )
					if choice == 'Language Detection':
						st.write(f'** Language Detected -> ** { lang_reverse[ blob.detect_language() ] }')
					elif choice == 'Language Translation':
						lang_name: str = col_1.selectbox(label = 'Choose Language to Translate', options = list(languages.keys()) )
						st.write(f"** { sentence.title() } -> ** { blob.translate(to = languages[lang_name]) }")
					elif choice == 'Spelling Correction':
						st.write(f"** { sentence.title() } -> ** { blob.correct() }")
					elif choice == 'Sentiment Analysis':
						polarity, subjectivity = blob.sentiment
						polarity, subjectivity = round(float(polarity), 2), round(float(subjectivity), 2)
						sentiment: str = 'Positive' if polarity >= 0.1 else 'Negative' if polarity <= -0.1 else 'Neutral'
						st.write(f"** { sentence.title() } -> ** { sentiment }")
						st.write(f'** Score -> ** Polarity : { polarity } | Subjectivity : { subjectivity } ')
					elif choice == 'Synonyms Antonyms':
						keyword: str = col_1.text_input(label = 'Enter Keyword to Get Definition, Synonyms, Antonyms')
						if keyword is not None:
							synonyms, antonyms, text_word = set(), set(), Word( keyword.title() )
							st.write(f'** Word Definition -> ** { text_word.definitions }')
							for synset in text_word.synsets:
								for lemma in synset.lemmas():
									if lemma.antonyms():
										antonyms.add( lemma.antonyms()[0].name() )
									synonyms.add( lemma.name() )
							st.write(f'** Synonyms : ** { synonyms }')
							st.write(f'** Antonyms : ** { antonyms }')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'OpenWhyd':
			try:
				st.subheader('** OpenWhyd **')
				col_1, col_2 = st.columns((2, 2))
				st.write('Openwhyd is a Free and Open Source Music Curation Service That Allows Users to Create Playlists of \
					Music Tracks from Various Streaming Platforms (YouTube, SoundCloud, Vimeo etc).')
				genre: str = col_1.selectbox(label = 'Select Genre', options = ('ALL', 'Blues', 'Classical', 'Electro', 'Folk', 
					'Hip Hop', 'Indie', 'Jazz', 'Latin', 'Metal', 'Pop', 'Punk', 'Reggae', 'Rock', 'Soul', 'World') )
				limit: int = col_2.slider(label = 'How Many Posts ?', min_value = 5, max_value = 1000, value = 5, step = 5)
				if genre is not None and limit is not None:
					response: dict = requests.get(url = f'https://openwhyd.org/hot/{genre}?format=json&limit={limit}').json()
					st.write(f'** Selected Genre : ** { genre } ** | Limit : ** { limit } ')
					for data in response.get('tracks'):
						st.write(f"** Name : ** { data.get('name', 'TBD') }")
						video_link: str = f"https://youtube.com/embed/{ data.get('eId', 'TBD').split('/')[-1] }"
						st.markdown(body = f"<iframe width = 400 height = 300 src = '{ video_link }' frameborder = 0 allow = 'accelerometer; \
							autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen> </iframe>", unsafe_allow_html = True)
						st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Gold Silver Price':
			try:
				st.subheader('** Gold Silver Price in India **')
				col_1, col_2 = st.columns((2, 2))
				cities: tuple = ('Ahmedabad', 'Bangalore', 'Bhubaneswar', 'Chandigarh', 'Chennai', 'Coimbatore', 'Delhi', 
					'Hyderabad', 'Jaipur', 'Kerala', 'Kolkata', 'Lucknow', 'Madurai', 'Mangalore', 'Mumbai', 'Mysore', 
					'Nagpur', 'Nashik', 'Patna', 'Pune', 'Surat', 'Vadodara', 'Vijayawada', 'Visakhapatnam')
				gold_silver_option: str = col_1.selectbox(label = 'Gold / Silver Price ?', options = ('Gold', 'Silver') )
				city_name: str = col_2.selectbox(label = 'Select Indian City', options = cities )
				if gold_silver_option == 'Gold' and city_name:
					dataset = pandas.read_html(f'https://goodreturns.in/gold-rates/{city_name.lower()}.html')
					st.write(f'** Today 22 & 24 Carat Gold Price Per Gram in { city_name } (INR) **')
					for index, data in enumerate( dataset[0:3] ):
						if index == 2:	st.write(f'** Gold Rate in { city_name } for Last 10 Days (10 g) **')
						new_header = data.iloc[0]
						data = data[1:]
						data.columns = new_header
						st.dataframe( data = data )
					for data in dataset[3:]:
						month = data.iloc[0, 0].split(' ')[-2]
						st.write(f'** Gold Price Movement in { city_name } | { month } **')
						st.dataframe( data = data )
				elif gold_silver_option == 'Silver' and city_name:
					dataset = pandas.read_html(f'https://goodreturns.in/silver-rates/{city_name.lower()}.html')
					st.write(f'** Today Silver Price Per Gram / KG in { city_name } (INR) **')
					for index, data in enumerate( dataset[0:2] ):
						if index == 1:	st.write(f'** Silver Rate in { city_name } for Last 10 Days **')
						new_header = data.iloc[0]
						data = data[1:]
						data.columns = new_header
						st.dataframe( data = data )
					for data in dataset[2:]:
						month = data.iloc[0, 0].split(' ')[-2]
						st.write(f'** Silver Price Movement in { city_name } | { month } **')
						st.dataframe( data = data )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Fuel Price':
			try:
				st.subheader('** Fuel Price in India **')
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				states: tuple = ('Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 
					'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'West Bengal',
					'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 
					'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand')
				petrol_diesel_option: str = col_1.selectbox(label = 'Fuel / Gas Type ?', options = ('Petrol', 'Diesel', 'LPG') )
				state_name: str = col_2.selectbox(label = 'Select Indian State', options = states )
				if petrol_diesel_option == 'Petrol' and state_name:
					dataset_1 = pandas.read_html(f"https://petroldieselprice.com/{state_name.replace(' ', '-')}-petrol-rate")
					st.write(f'** Petrol Price in { state_name } Today **')
					st.dataframe( data = dataset_1[0] )
					st.write(f'** Historical Petrol Price in { state_name } **')
					st.dataframe( data = dataset_1[2] )
					dataset_1[3].fillna('TBD', inplace = True)
					cities: list = [city.replace(' Petrol Price', '') for city in reduce(lambda x, y: x + y, dataset_1[3].values.tolist() ) if str(city) != 'TBD']
					city_name: str = col_3.selectbox(label = f'Select City in { state_name }', options = cities )
					dataset_2 = pandas.read_html(f"https://petroldieselprice.com/petrol-rate-in-{city_name.replace(' ', '-')}")
					st.write(f'** Petrol Price in { city_name } Today **')
					st.dataframe( data = dataset_2[0] )
					st.write(f'** Historical Petrol Price in { city_name } **')
					st.dataframe( data = dataset_2[2] )
				elif petrol_diesel_option == 'Diesel' and state_name:
					dataset_1 = pandas.read_html(f"https://petroldieselprice.com/{state_name.replace(' ', '-')}-diesel-rate")
					st.write(f'** Diesel Price in { state_name } Today **')
					st.dataframe( data = dataset_1[0] )
					st.write(f'** Historical Diesel Price in { state_name } **')
					st.dataframe( data = dataset_1[2] )
					dataset_1[3].fillna('TBD', inplace = True)
					cities: list = [city.replace(' Diesel Price', '') for city in reduce(lambda x, y: x + y, dataset_1[3].values.tolist() ) if str(city) != 'TBD']
					city_name: str = col_3.selectbox(label = f'Select City in { state_name }', options = cities )
					dataset_2 = pandas.read_html(f"https://petroldieselprice.com/diesel-rate-in-{city_name.replace(' ', '-')}")
					st.write(f'** Diesel Price in { city_name } Today **')
					st.dataframe( data = dataset_2[0] )
					st.write(f'** Historical Diesel Price in { city_name } **')
					st.dataframe( data = dataset_2[2] )
				elif petrol_diesel_option == 'LPG' and state_name:
					dataset_1 = pandas.read_html(f"https://petroldieselprice.com/{state_name.replace(' ', '-')}-LPG-cylinder-rate")
					st.write(f'** LPG Cylinder Price in { state_name } Today **')
					st.dataframe( data = dataset_1[0] )
					dataset_1[1].fillna('TBD', inplace = True)
					cities: list = [city for city in reduce(lambda x, y: x + y, dataset_1[1].values.tolist() ) if str(city) != 'TBD']
					city_name: str = col_3.selectbox(label = f'Select City in { state_name }', options = cities )
					dataset_2 = pandas.read_html(f"https://petroldieselprice.com/LPG-cylinder-rate-in-{city_name.replace(' ', '-')}")
					st.write(f'** LPG Cylinder Price in { city_name } Today **')
					st.dataframe( data = dataset_2[0] )
					st.write(f'** Recent Revised LPG Cylinder Price in { city_name } **')
					st.dataframe( data = dataset_2[1] )
					st.write(f'** Historical Trend - LPG Cylinder Price in { city_name } **')
					st.dataframe( data = dataset_2[2] )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Fuel Price India':
			try:
				st.subheader('** Fuel Price in India **')
				col_1, col_2, col_3, col_4 = st.columns((2, 2, 2, 2))
				category: str = col_1.selectbox(label = 'Fuel Cost / Distance ?', options = ['Fuel Cost', 'Distance'])
				fuel_cost_liter: int = col_2.number_input('Petrol / Diesel Rs. / Litre', min_value = 1, max_value = 99999, value = 100, step = 1)
				vehicle_milage: int = col_3.number_input('Vehicle Milage (KMPL)', min_value = 1, max_value = 99999, value = 10, step = 1)
				if category == 'Fuel Cost':
					fuel_cost: int = col_4.number_input('Petrol / Diesel Price (Rs.)', min_value = 1, max_value = 99999, value = 500, step = 1)
					st.write(f'** Fuel Cost Rs. = { fuel_cost } | Vehicle Milage = { vehicle_milage } KMPL **')	
					fuel_litres: float = round(fuel_cost / fuel_cost_liter, 2)
					distance: float = round(fuel_litres * vehicle_milage, 2)
					st.write(f'** Total Fuel { fuel_litres } Litres | Total Distance { distance } KM **')
				elif category == 'Distance':
					distance: int = col_4.number_input('Distance (KM)', min_value = 1, max_value = 99999, value = 90, step = 1)
					st.write(f'** Distance = { distance } KM | Vehicle Milage = { vehicle_milage } KMPL **')	
					fuel_litres: float = round(distance / vehicle_milage, 2)
					fuel_cost: float = round(fuel_litres * fuel_cost_liter, 2)
					st.write(f'** Total Fuel { fuel_litres } Litres | Total Fuel Cost Rs. { fuel_cost } **')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'World Countries':
			try:
				st.subheader('** World Countries **')
				col_1, col_2 = st.columns((2, 2))
				category: str = col_1.selectbox(label = 'World Countries / USA States ?', options = ['Countries', 'USA States'])
				dataset = pandas.DataFrame( World_Countries( category ) )
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				if category == 'Countries':
					countries: list = col_2.multiselect(label = 'Select World Countries', 
						options = list(dataset.name.unique()), default = ['United States', 'India'] )
					dataset = dataset[ dataset.name.isin( countries ) ]
				elif category == 'USA States':
					usa_states: list = col_2.multiselect(label = 'Select USA States', 
						options = list(dataset.name.unique()), default = ['California'] )
					dataset = dataset[ dataset.name.isin( usa_states ) ]
				st.dataframe( data = dataset )
				st.map( data = dataset, zoom = 2)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Google Search':
			try:
				st.subheader('** Google Search **')
				keyword: str = st.text_input(label = 'Enter Keyword to Search in Google', value = 'Python Programming')
				payload: dict = {'access_key': '744253598ee227f505195ea97bcb17b0', 'query': keyword }
				## Google Domains List = https://serpstack.com/resource.google.domains.csv
				## Google Countries List = https://serpstack.com/resource.google.countries.csv
				## Google Languages List = https://serpstack.com/resource.google.languages.csv
				response: dict = requests.get(url = 'http://api.serpstack.com/search', params = payload).json()
				st.write(f"** Web Page Results ** \
					Total Results : { response.get('search_information', 'TBD').get('total_results', 'TBD') } | \
					Time Taken to Display : { response.get('search_information', 'TBD').get('time_taken_displayed', 'TBD') } Seconds.")
				for data in response['organic_results']:
					st.write(f"** # { data.get('title', 'TBD') } **")
					st.markdown(body = f" <a href = { data.get('url', 'TBD') } target = '_blank'> Web Page Link </a> ", unsafe_allow_html = True)
					st.write(f"** Description : ** { data.get('snippet', 'TBD') }")
					st.write('*' * 100)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Other Tools':
			try:
				st.subheader('** Other Tools **')
				col_1, col_2 = st.columns((2, 2))
				Tools: tuple = ('Random Password Generator', 'Secure Hash Algorithms', 'QR Code Generator')
				Tool: str = st.selectbox(label = 'Choose Tool', options = Tools)
				if Tool == 'Random Password Generator':
					input_length: int = col_2.number_input('Choose the Length', min_value = 6, max_value = 20, value = 8, step = 1)
					result: str = ''.join( random.choice(string.digits + string.ascii_lowercase + \
						string.ascii_uppercase + string.punctuation) for i in range(input_length) )
					st.write(f'** Result : ** { result }')
				elif Tool == 'Secure Hash Algorithms':
					st.write('''**Secure Hash Algorithms ** (SHA) are Set of Cryptographic Hash Functions Defined By The
						Language To Be Used For Various Applications Such as Password Security etc..''')
					keyword: str = col_2.text_input(label = 'Enter the Keyword to hash', value = '')
					if keyword is not None:
						st.write(f'** Input Keyword : ** { keyword }')
						st.write(f'** SHA 1 : ** { hashlib.sha1(keyword.encode()).hexdigest() }')
						st.write(f'** SHA 224 : ** { hashlib.sha224(keyword.encode()).hexdigest() }')
						st.write(f'** SHA 256 : ** { hashlib.sha256(keyword.encode()).hexdigest() }')
						st.write(f'** SHA 384 : ** { hashlib.sha384(keyword.encode()).hexdigest() }')
						st.write(f'** SHA 512 : ** { hashlib.sha512(keyword.encode()).hexdigest() }')
						st.write(f'** MD5 : ** { hashlib.md5(keyword.encode()).hexdigest() }')
				elif Tool == 'QR Code Generator':
					keyword: str = st.text_area(label = 'Enter Text / URL', value = '', height = 5)
					if keyword is not None:
						output = BytesIO()
						img = qrcode.make( keyword )
						img.save(output)
						processed_data = output.getvalue()
						st.image( image = processed_data, width = 300, use_column_width = False )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Coin Market Cap':
			try:
				st.subheader('** Coin Market Cap **')
				col_1, col_2, col_3, col_4 = st.columns((2, 2, 2, 2))
				st.write('CoinMarketCap: Cryptocurrency Prices, Charts And Market..')
				sub_cat: str = col_3.selectbox(label = 'Crypto Currencies / Crypto Currencies Exchanges ?', 
					options = ('Crypto Currencies', 'Crypto Currencies Exchanges'))
				if sub_cat == 'Crypto Currencies':
					currencies = pandas.read_html('https://coinmarketcap.com/all/views/all/')[2]	
					st.markdown( data = Excel_Downloader( currencies ), unsafe_allow_html = True)
					if st.checkbox('Wanna See the Crypto Currencies List ?'):	st.dataframe( data = currencies )
					currency: str = col_1.selectbox(label = 'Select Crypto Currency', options = list(currencies.Name.unique()) )
					start_date: str = col_2.date_input('Start Date', (datetime.now() - timedelta(days = 30)) )
					end_date: str = col_4.date_input('End Date', datetime.now() )
					st.write(f'** Selected Currency : ** { currency } ** | Start Date : ** { start_date } ** |\
						End Date : ** { end_date }')
					dataset_1, dataset_2 = Crypto_Currencies( currency.lower().replace(' ', '-'), \
						start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d') )
					st.markdown( data = Excel_Downloader( dataset_1 ), unsafe_allow_html = True)
					st.dataframe( data = dataset_1.style.highlight_max(axis = 0) )
					st.write(f'** { currency } Statistics **')
					st.dataframe( data = dataset_2 )
				elif sub_cat == 'Crypto Currencies Exchanges':
					exchanges = pandas.read_html('https://coinmarketcap.com/rankings/exchanges/')[2]
					st.markdown( data = Excel_Downloader( exchanges ), unsafe_allow_html = True)
					if st.checkbox('Wanna See the Crypto Currencies Exchange List ?'):	st.dataframe( data = exchanges )
					exchange: str = col_1.selectbox(label = 'Select Crypto Currency Exchange', options = list(exchanges.Name.unique()) )
					exchange_name: str = exchange.lower().replace(' ', '-').replace('.', '-')
					dataset = pandas.read_html(f'https://coinmarketcap.com/exchanges/{exchange_name}')[2]
					st.markdown( data = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'NBA Stats V2':
			try:
				st.subheader('** NBA Stats V2 **')
				col_1, col_2 = st.columns((2, 2))
				nba_teams: dict = requests.get('https://balldontlie.io/api/v1/teams').json().get('data', 'TBD')
				if nba_teams != 'TBD':
					sub_category: str = col_1.selectbox(label = 'Choose Sub Category', options = ['NBA Teams', 'NBA Players'])
					if sub_category == 'NBA Teams':
						st.markdown( body = Excel_Downloader( pandas.DataFrame( nba_teams ) ), unsafe_allow_html = True)
						st.dataframe( data = pandas.DataFrame( nba_teams ) )
					elif sub_category == 'NBA Players':
						team_name: str = col_2.selectbox(label = 'Select NBA Team', options = [data['full_name'] for data in nba_teams] )
						st.write(f'** Selected NBA Team ** : { team_name }')
						dataset = pandas.DataFrame( List_NBA_Players(team_name = team_name) )
						st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
						st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Google News 1':
			try:
				st.subheader('** Google News 1 **')
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				keyword: str = col_3.text_input(label = 'Enter Keyword', value = '')
				start_date: str = col_1.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 30)) )
				end_date: str = col_2.date_input(label = 'End Date', value = datetime.now() )
				if keyword and start_date and end_date:
					googlenews = GoogleNews(lang = 'en', encode = 'utf-8', 
						start = start_date.strftime('%m/%d/%Y'), end = end_date.strftime('%m/%d/%Y'))
					googlenews.search( keyword.upper() )
					for data in googlenews.result():
						st.write(f"** Title : ** { data.get('title', 'TBD') } ")
						st.write(f"** Media / Published Date : ** { data.get('media', 'TBD') } / { data.get('date', 'TBD') } ")
						st.write(f"** Description : ** { data.get('desc', 'TBD') } ")
						st.markdown(body = f"<a href = '{ data['link'] }' target = '_blank'> More Details, Click Here! </a> ", unsafe_allow_html = True)
						st.write( '*' * 50 )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Google News 2':
			try:
				st.subheader('** Google News 2 **')
				keyword: str = st.text_input(label = 'Enter Keyword', value = '')
				if keyword is not None and len( keyword ) > 0:
					keyword: str = keyword.replace(' ', '+').lower()
					NewsFeed: dict = feedparser.parse(f'https://news.google.com/rss/search?q={keyword}')
					for data in NewsFeed.get('entries'):
						with st.expander(label = data.get('title', 'TBD') , expanded = False):
							st.json(body = data)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'National Today':
			try:
				st.subheader('** National Today **')
				st.write('List of Holidays and Special Moments on this Cultural Calendar..')
				month_name: str = st.selectbox(label = 'Choose Month', options = [calendar.month_name[i] for i in range(1, 13)])
				dataset = pandas.read_html(f'https://nationaltoday.com/{month_name.lower()}-holidays/')[0]
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'DuckDuckGo Search':
			try:
				st.subheader('** DuckDuckGo Search Engine **')
				st.write('Internet Search Engine that Emphasizes Protecting Searchers Privacy & Avoiding the Filter Bubble of Personalized Search Results.')
				keyword: str = st.text_input(label = 'Enter Keyword', value = 'Programming')
				response: dict = requests.get(f"https://api.duckduckgo.com/?q={keyword.replace(' ', '+').title()}&format=json&pretty=1").json()
				st.write(f"** Title : ** { response.get('Heading', 'TBD') } ")
				st.write(f"** Source / Entity : ** { response.get('AbstractSource', 'TBD') } / { response.get('Entity', 'TBD') } ")
				st.write(f"** Description : ** { response.get('Abstract', 'TBD') }")
				st.write(f"** URL : ** { response.get('AbstractURL', 'TBD') }")
				for data in response.get('Results'):
					st.write(f"** => Text : ** { data.get('Text', 'TBD') } ")
					st.write(f"** => URL : ** { data.get('FirstURL', 'TBD') } ")
					if 'Icon' in data.keys() and len( data['Icon'].get('URL') ) > 0:
						st.markdown(body = f"<img class = 'rounded-circle article-img' src='{data['Icon']['URL'] }' \
							width = 200 height = 200>", unsafe_allow_html = True )
					st.write( '*' * 50 )
				for data in response.get('RelatedTopics'):
					if 'Topics' in data.keys():
						for topic in data.get('Topics'):
							st.write(f"** => Text : ** { topic.get('Text', 'TBD') } ")
							st.write(f"** => URL : ** { topic.get('FirstURL', 'TBD') } ")
							if 'Icon' in topic.keys() and len( topic['Icon'].get('URL') ) > 0:
								st.markdown(body = f"<img class = 'rounded-circle article-img' src='{topic['Icon']['URL'] }' \
									width = 200 height = 200>", unsafe_allow_html = True )
							st.write( '*' * 50 )
					st.write(f"** => Text : ** { data.get('Text', 'TBD') } ")
					st.write(f"** => URL : ** { data.get('FirstURL', 'TBD') } ")
					if 'Icon' in data.keys() and len( data['Icon'].get('URL') ) > 0:
						st.markdown(body = f"<img class = 'rounded-circle article-img' src='{data['Icon']['URL'] }' \
							width = 200 height = 200>", unsafe_allow_html = True )
					st.write( '*' * 50 )
				with st.expander('Show JSON Content', expanded = False):
					st.json( body = response )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Streamlit Apps':
			try:
				st.subheader('** Akashjeez - Streamlit Apps **')
				BASE_URL: str = 'https://share.streamlit.io/akashjeez/Streamlit-Apps/main/{}'
				st.markdown(body = f'''
					<a href = '{ BASE_URL.format('PySportz.py') }' target = '_blank'> App 1 | Sports League </a> <br/>
					<a href = '{ BASE_URL.format('PyOpenCV.py') }' target = '_blank'> App 2 | Image & Video Analytics </a> <br/>
				''', unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Send Free SMS':
			try:
				st.subheader('** Send Free SMS **')
				col_1, col_2 = st.columns((2, 2))
				test_keys: dict = {'api_key': '6EOF0X9BQO31UX6VHFKLK9CKVTY8Y5SL', 'secret_key': 'P0TQGUECQTN2L98W', 'type': 'stage'}
				live_keys: dict = {'api_key': '0CJIHPGPT95YI8M6CLGROPMNGGQCCG58', 'secret_key': '8JZOEO4VJ298P7MQ', 'type': 'prod' }
				recepient_num: str = col_1.text_input(label = 'Enter Recipient Number (Without +91)', value = '')
				message: str = col_2.text_area(label = 'Enter Your Message', value = '')
				if recepient_num is not None and message is not None:
					params: dict = { 'apiKey': test_keys.get('api_key'), 'secret': test_keys.get('secret_key'),
						'useType': test_keys.get('type'), 'phone': recepient_num, 'message': message.strip(), 'senderid': 'akashit'}
					response = requests.post(url = 'https://sms4india.com/api/v1/sendCampaign', data = params)
					if response.status_code >= 200 and response.status_code < 300:
						st.write(f'Message Sent to +91{recepient_num} Sucessfully!')
					else:
						st.write('Message Sending Failed!')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Wikipedia Search':
			try:
				st.subheader('** Wikipedia Search **')
				keyword: str = st.text_input(label = 'Enter Keyword to Search', value = '')
				if keyword is not None and len( keyword ) > 0:
					st.write(f'** Input Keyword = ** { keyword } ')
					for data in wikipedia.summary(keyword.title()).splitlines():
						st.write( data )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'WikiQuote':
			try:
				st.subheader('** WikiQuote **')
				keyword: str = st.text_input(label = 'Enter Keyword to Search', value = '')
				if keyword is not None and len( keyword ) > 0:
					st.write(f'** Input Keyword = ** { keyword } ')
					for data in wikiquote.quotes(keyword.title()):
						st.write( data )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Text to Speech':
			try:
				st.subheader('** Text to Speech **')
				language: str = col_3.selectbox(label = 'Select Language', options = [key for key,_ in LANGUAGES.items()])
				input_text: str = st.text_area(label = 'Enter Your Text')
				if input_text is not None and language is not None:
					mp3_file = BytesIO()
					tts = gTTS(text = input_text, lang = LANGUAGES[language])
					tts.write_to_fp(fp = mp3_file)
					st.audio(data = mp3_file, format = 'audio/mpeg')
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Phone Number Tracker':
			try:
				st.subheader('** Phone Number Tracker **')
				col_1, col_2 = st.columns((2, 2))
				ph_number: str = col_1.text_input(label = 'Enter Phone Number with Country Code', value = '')
				Countries: dict = { data['name'] : data['alpha2Code']  for data in \
					requests.get(url = 'https://restcountries.eu/rest/v2/all').json() }
				Country: str = col_2.selectbox(label = 'Choose Country Name', options = list(Countries.keys()) )
				if len(ph_number) > 0 and Country:
					phone_no = phonenumbers.parse(number = ph_number, region = Countries[Country])
					st.write(f'** Timezone = ** { timezone.time_zones_for_number(numobj = phone_no) } ')
					st.write(f"** Country = ** { geocoder.description_for_number(numobj = phone_no, lang = 'en') } ")
					st.write(f"** Service Provider = ** { carrier.name_for_number(numobj = phone_no, lang = 'en') } ")
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'Protect PDF':
			try:
				st.subheader('** Protect PDF **')
				col_1, col_2 = st.columns((4, 2))
				pdf_file = col_1.file_uploader(label = 'Select PDF File', type = ['PDF'])
				category: str = col_2.selectbox(label = 'Select PDF Category', options = (
					'View PDF', 'Set Password', 'Remove Password') )
				if pdf_file is not None and category == 'View PDF':
					pdf_reader = PdfFileReader( BytesIO( pdf_file.read() ) )
					st.write( { 'File_Name': pdf_file.name, 'File_Type': pdf_file.type, 
						'File_Size': Convert_Size( pdf_file.size ), 'Total_Pages': pdf_reader.numPages } )
					base64_pdf = base64.b64encode( open(file = pdf_file, mode = 'rb').read() ).decode('utf-8')
					st.markdown(body = f"<embed src = 'data:application/pdf;base64,{base64_pdf}' \
						width = 700 height = 1000 type = 'application/pdf'>", unsafe_allow_html = True)
			except Exception as ex:
				st.error(f'** Error : { ex } **')

		elif SUB_CATEGORY == 'CoVaccine India':
			try:
				st.subheader('** CoVaccine India **')
				st.markdown(body = f"Find Appointment Availabilty & Download Vaccination Certificates. Vaccine Drive \
					<a href = 'https://cowin.gov.in/' target = '_blank'> Link </a>", unsafe_allow_html = True)
				BASE_URL: str = 'https://cdn-api.co-vin.in/api/v2'
				HEADERS: dict = { 'accept': 'application/json' ,'Accept-Language': 'en_US', 'User-Agent': UserAgent().random }
				Categories: tuple = ('List States', 'List Districts', 'Get Vaccination Sessions by Pin', 'Get Vaccination Sessions by District', 
					'Get Vaccination Sessions by Pin for 7 Days', 'Get Vaccination Sessions by District for 7 Days')
				Category: str = st.selectbox( label = 'Choose Category', options = Categories )
				col_1, col_2, col_3 = st.columns((2, 2, 2))
				if Category == 'List States':
					response: dict = requests.get(url = f'{ BASE_URL }/admin/location/states', headers = HEADERS).json()
					if 'states' in response.keys():
						st.dataframe( data = response['states'] )
				elif Category == 'List Districts':
					States: dict = requests.get(url = f'{ BASE_URL }/admin/location/states', headers = HEADERS).json()
					States: dict = { data['state_name'] : data['state_id'] for data in States['states'] }
					State_Name: str = col_1.selectbox( label = 'Select State', options = list(States.keys()) )
					response: dict = requests.get(url = f"{ BASE_URL }/admin/location/districts/{ States[State_Name] }", headers = HEADERS).json()
					if 'districts' in response.keys():
						st.dataframe( data = response['districts'] )
				elif Category == 'Get Vaccination Sessions by Pin':
					PIN_Code: int = col_1.number_input(label = 'Enter PIN Code', min_value = 1, max_value = 999999999, step = 1)
					Date: str = col_2.date_input(label = 'Choose Date', value = datetime.now() )
					if PIN_Code is not None and Date is not None:
						Date: str = Date.strftime('%d-%m-%Y')
					request_url: str = f'{ BASE_URL }/appointment/sessions/public/findByPin?pincode={ PIN_Code }&date={ Date }'
					response: dict = requests.get(url = request_url, headers = HEADERS).json()
					if 'sessions' in response.keys():
						st.dataframe( data = response['sessions'] )
				elif Category == 'Get Vaccination Sessions by District':
					States: dict = requests.get(url = f'{ BASE_URL }/admin/location/states', headers = HEADERS).json()
					States: dict = { data['state_name'] : data['state_id'] for data in States['states'] }
					State_Name: str = col_1.selectbox( label = 'Select State', options = list(States.keys()) )
					Districts: dict = requests.get(url = f'{ BASE_URL }/admin/location/districts/{ States[State_Name] }', headers = HEADERS).json()
					Districts: dict = { data['district_name'] : data['district_id'] for data in Districts['districts'] }
					District_Name: str = col_2.selectbox( label = 'Select District', options = list(Districts.keys()) )
					Date: str = col_3.date_input(label = 'Choose Date', value = datetime.now() )
					if District_Name is not None and Date is not None:
						Date: str = Date.strftime('%d-%m-%Y')
						request_url: str = f'{ BASE_URL }/appointment/sessions/public/findByDistrict?district_id={Districts[District_Name]}&date={Date}'
						response: dict = requests.get(url = request_url, headers = HEADERS).json()
						if 'sessions' in response.keys():
							st.dataframe( data = response['sessions'] )
				elif Category == 'Get Vaccination Sessions by Pin for 7 Days':
					PIN_Code: int = col_1.number_input(label = 'Enter PIN Code', min_value = 1, max_value = 999999999, step = 1)
					Start_Date: str = col_2.date_input(label = 'Choose Start Date', value = datetime.now() )
					if PIN_Code is not None and Start_Date is not None:
						Date: str = Start_Date.strftime('%d-%m-%Y')
						request_url: str = f'{ BASE_URL }/appointment/sessions/public/calendarByPin?pincode={ PIN_Code }&date={ Date }'
						response: dict = requests.get(url = request_url, headers = HEADERS).json()
						if 'centers' in response.keys():
							for data in response.get('centers'):
								with st.expander(label = data.get('name', 'TBD'), expanded = False):
									dataset: list = copy.copy( data )
									del dataset['sessions']
									st.dataframe( data = list( dataset.items() ) )
									if 'sessions' in data.keys() and len( data['sessions'] ) > 0:
										for sessions in data.get('sessions'):
											st.dataframe( data = sessions )
				elif Category == 'Get Vaccination Sessions by District for 7 Days':
					States: dict = requests.get(url = f'{ BASE_URL }/admin/location/states', headers = HEADERS).json()
					States: dict = { data['state_name'] : data['state_id'] for data in States['states'] }
					State_Name: str = col_1.selectbox( label = 'Select State', options = list(States.keys()) )
					Districts: dict = requests.get(url = f'{ BASE_URL }/admin/location/districts/{ States[State_Name] }', headers = HEADERS).json()
					Districts: dict = { data['district_name'] : data['district_id'] for data in Districts['districts'] }
					District_Name: str = col_2.selectbox( label = 'Select District', options = list(Districts.keys()) )
					Date: str = col_3.date_input(label = 'Choose Date', value = datetime.now() )
					if District_Name is not None and Date is not None:
						Date: str = Date.strftime('%d-%m-%Y')
						request_url: str = f'{ BASE_URL }/appointment/sessions/public/calendarByDistrict?district_id={Districts[District_Name]}&date={Date}'
						response: dict = requests.get(url = request_url, headers = HEADERS).json()
						if 'centers' in response.keys():
							for data in response.get('centers'):
								with st.expander(label = data.get('name', 'TBD'), expanded = False):
									dataset: list = copy.copy( data )
									del dataset['sessions']
									st.dataframe( data = list( dataset.items() ) )
									if 'sessions' in data.keys() and len( data['sessions'] ) > 0:
										for sessions in data.get('sessions'):
											st.dataframe( data = sessions )
			except Exception as ex:
				st.error(f'** Error : { ex } **')

#--------------------------------------------------------------------------------------------------------------------------------------#

## https://searchcode.com/api/

## Run the Main Code!

if __name__ == '__main__':
	Execute_Main()

#--------------------------------------------------------------------------------------------------------------------------------------#
