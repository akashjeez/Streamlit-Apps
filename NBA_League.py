__author__ = 'akashjeez'

import os, io, base64, pandas, requests
from datetime import datetime, timedelta
# from fake_useragent import UserAgent
import streamlit as st


#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('NB@😎L€@gU€')

#----------------------------------------------------------------------------------------------------------------------#

## Reference => https://github.com/swar/nba_api/blob/master/docs/table_of_contents.md

BASE_URL = 'https://stats.nba.com'

STATIC_HEADERS = {
	'Host': 'stats.nba.com', 
	#'User-Agent': UserAgent().random,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
	'Accept': 'application/json, text/plain, */*', 
	'Accept-Language': 'en-US,en;q=0.5', 
	'Accept-Encoding': 'gzip, deflate, br', 
	'x-nba-stats-origin': 'stats', 'x-nba-stats-token': 'true', 
	'Connection': 'keep-alive', 'Referer': BASE_URL, 
	'Pragma': 'no-cache', 'Cache-Control': 'no-cache'
}

CATEGORIES_LIST: list = ['About NBA', 'NBA Teams', 'NBA Players', 'NBA Player Profile', 'NBA ScoreBoard',
	'NBA League Players', 'NBA League Standings', 'NBA All Time Leaders', 'NBA Team Yearly Stats']
CATEGORIES_LIST.sort()

#----------------------------------------------------------------------------------------------------------------------#

def Excel_Downloader(df: pandas.DataFrame) -> str:
	output = io.BytesIO()
	writer = pandas.ExcelWriter(path = output, engine = 'xlsxwriter')
	df.to_excel(excel_writer = writer, sheet_name = 'Data', index = False)
	writer.save()
	processed_data = output.getvalue()
	b64 = base64.b64encode(processed_data)
	return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"


@st.cache
def List_NBA_Teams() -> dict:
	try:
		response = requests.get('https://balldontlie.io/api/v1/teams').json()
		dataset: list = [ {
			'Team_Code': data.get('abbreviation', 'TBD'), 'Team_City': data.get('city', 'TBD'),
			'Team_Name': data.get('name', 'TBD'), 'Team_Full_Name': data.get('full_name', 'TBD'),
			'Team_Conference': data.get('conference', 'TBD'), 'Team_Division': data.get('division', 'TBD'),
		} for data in response['data'] ]
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Players(team_name: str) -> dict:
	try:
		BASE_URL, dataset = 'https://balldontlie.io/api', []
		temp_response: dict = requests.get(f'{BASE_URL}/v1/players').json()
		total_pages: int = temp_response.get('meta', 'TBD').get('total_pages', 1)
		for i in range(1, int(total_pages) + 1):
			response = requests.get(f'{BASE_URL}/v1/players?page={i}').json()
			for data in response['data']:
				if data['team']['full_name'] == team_name:
					data_dump: dict = {
						'Player_ID': data.get('id', 'TBD'),
						'Player_Name': f"{ data.get('first_name', 'TBD') } {data.get('last_name', 'TBD') }",
						'Position': data['position'] if 'position' in data.keys() else 'TBD',
					}
					if team := data['team']:
						data_dump.update({
							'Team_Code': team.get('abbreviation', 'TBD'), 'Team_City': team.get('city', 'TBD'),
							'Team_Name': team.get('name', 'TBD'), 'Team_Full_Name': team.get('full_name', 'TBD'),
							'Team_Conference': team.get('conference', 'TBD'), 'Team_Division': team.get('division', 'TBD'),
						})
					dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_Player_Profile(player_id: int) -> dict:
	try:
		payloads = { 'PerMode': 'Totals', 'PlayerID': player_id }
		request_url = f'{BASE_URL}/stats/playerprofilev2?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_League_Players() -> dict:
	try:
		season_year = f"{ ( datetime.now() - timedelta(days = 365)).year }-{ str( datetime.now().year )[2:] }"
		payloads = { 'IsOnlyCurrentSeason': 0, 'LeagueID': '00', 'Season': season_year }
		request_url = f'{BASE_URL}/stats/commonallplayers?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_Live_Scoreboard(game_date: str) -> dict:
	try:
		payloads = { 'DayOffset': 0, 'LeagueID': '00', 'GameDate': game_date }
		request_url = f'{BASE_URL}/stats/scoreboard?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_League_Standings() -> dict:
	try:
		season_year = f"{ ( datetime.now() - timedelta(days = 365)).year }-{ str( datetime.now().year )[2:] }"
		payloads = { 'LeagueID': '00', 'Season': season_year, 'SeasonType' : 'Regular+Season' }
		request_url = f'{BASE_URL}/stats/leaguestandings?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_Player_Awards(player_id: int) -> dict:
	try:
		request_url = f'{BASE_URL}/stats/playerawards?PlayerID={player_id}'
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_Alltime_Leaders(limit: int) -> dict:
	try:
		payloads = { 'LeagueID': '00', 'PerMode': 'Totals', 'SeasonType': 'Regular+Season', 'TopX': int(limit)}
		request_url = f'{BASE_URL}/stats/alltimeleadersgrids?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NBA_Team_YearByYear_Stats(team_id: int) -> dict:
	try:
		payloads = { 'LeagueID': '00', 'PerMode': 'Totals', 'SeasonType': 'Regular+Season', 'TeamID': int(team_id)}
		request_url = f'{BASE_URL}/stats/teamyearbyyearstats?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(request_url, headers = STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


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

	if CATEGORY == 'About NBA':
		st.subheader('** About NBA **')
		st.write("""The National Basketball Association (NBA) is an American Men's Professional Basketball League. It is 
			Composed of 30 Teams and is One of the 4 Major Professional Sports Leagues in the United States and Canada. 
			It is Widely Considered to be the Premier Men's Professional Basketball League in the World.""")
		st.markdown( f"<img src = 'https://wallpapercave.com/wp/wp1827442.jpg' width = 700 height = 400>", unsafe_allow_html = True )

	elif CATEGORY == 'NBA Teams':
		try:
			st.subheader('** NBA Teams **')
			col_1, col_2 = st.beta_columns((2, 2))
			dataset = pandas.DataFrame( data = List_NBA_Teams()['data'] )
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
			col_1.write('** NBA Teams by Division Split **')
			pivot_division = pandas.pivot_table(dataset, index = 'Team_Division', 
				values = 'Team_Name', aggfunc = 'count', fill_value = 0)
			col_1.dataframe( data = pivot_division )
			col_2.write('** NBA Teams by Conference Split **')
			pivot_conference = pandas.pivot_table(dataset, index = 'Team_Conference', 
				values = 'Team_Name', aggfunc = 'count', fill_value = 0)
			col_2.dataframe( data = pivot_conference )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA Players':
		try:
			st.subheader('** NBA Players **')
			NBA_Teams: list = [ data['Team_Full_Name'] for data in List_NBA_Teams()['data'] ]
			team_name: str = st.selectbox(label = 'Select NBA Team', options = NBA_Teams)
			dataset = pandas.DataFrame( List_NBA_Players( team_name = team_name )['data'] )
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA Player Profile':
		try:
			st.subheader('** NBA Player Profile **')
			col_1, col_2 = st.beta_columns((2, 2))
			st.write('Get Player ID by Search Name from Official NBA Stats -> https://stats.nba.com/players/')
			League_Players: dict =  NBA_League_Players()['resultSets'][0]
			player_names: list = [ data[2] for data in League_Players['rowSet'] ]
			player_name: str = col_1.selectbox(label = 'Choose NBA Player', options = player_names )
			player_id: list = [ data[0] for data in League_Players['rowSet'] if data[2] == player_name ][0]
			st.write(f'** NBA Player ID : ** { player_id } ** | Player Name : ** { player_name } ')
			Player_Profile: dict = NBA_Player_Profile( player_id  = player_id )
			st.write('** NBA Player Awards **')
			Player_Awards: dict = NBA_Player_Awards( player_id  = player_id )['resultSets'][0]
			Player_Awards = pandas.DataFrame( data = Player_Awards['rowSet'], columns = Player_Awards['headers'] )
			st.markdown( body = Excel_Downloader( df = Player_Awards ), unsafe_allow_html = True)
			st.dataframe( data = Player_Awards )
			titles: list = [ data['name'] for data in Player_Profile['resultSets'] ]
			sub_category: str = col_2.selectbox(label = 'Select Sub Category', options = titles )
			for data in Player_Profile['resultSets']:
				if sub_category == data['name']:
					st.write('** Sub Category ** : ', sub_category)
					data_frame = pandas.DataFrame( data = data['rowSet'], columns = data['headers'] )
					st.markdown( body = Excel_Downloader( df = data_frame ), unsafe_allow_html = True)
					st.dataframe( data = data_frame )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA League Players':
		try:
			st.subheader('** NBA All League Players **')
			League_Players =  NBA_League_Players()['resultSets'][0]
			dataset = pandas.DataFrame( data = League_Players['rowSet'], columns = League_Players['headers'] )
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA ScoreBoard':
		try:
			st.subheader('** NBA Live ScoreBoard **')
			col_1, col_2 = st.beta_columns((2, 2))
			game_date: str = col_1.date_input(label = 'Choose Game Date', value = datetime.now() )
			dataset: dict = NBA_Live_Scoreboard( game_date = game_date )
			titles: list = [ data['name'] for data in dataset['resultSets'] ]
			sub_category: str = col_2.selectbox(label = 'Select Sub Category', options = titles )
			for data in dataset['resultSets']:
				if sub_category == data['name']:
					st.write(f"** Selected Date | Sub Category : ** { game_date.strftime('%d-%b-%Y')  } | { sub_category } ")
					data_frame = pandas.DataFrame( data = data['rowSet'], columns = data['headers'] )
					st.markdown( body = Excel_Downloader( df = data_frame ), unsafe_allow_html = True)
					st.dataframe( data = data_frame )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA League Standings':
		try:
			st.subheader('** NBA League Standings **')
			col_1, col_2 = st.beta_columns((2, 2))
			data_dump = NBA_League_Standings()['resultSets'][0]
			dataset = pandas.DataFrame( data = data_dump['rowSet'], columns = data_dump['headers'] )
			filter_x = col_1.radio(label = 'Advanced Filter', options = ['ALL', 'Division', 'Conference'])
			if filter_x == 'ALL':
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			elif filter_x == 'Division':
				options = default = list( set( dataset.Division.unique() ) )
				division = col_2.multiselect(label = 'Select Division(s)', options = options, default = default )
				st.dataframe( dataset[ dataset.Division.isin(division) ] )
			elif filter_x == 'Conference':
				options = default = list( set( dataset.Conference.unique() ) )
				conference = col_2.multiselect(label = 'Select Conference(s)', options = options, default = default )
				st.dataframe( dataset[ dataset.Conference.isin(conference) ] )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA All Time Leaders':
		try:
			st.subheader('** NBA All Time Leaders **')
			headings = {'GPLeaders': 'Games Player', 'PTSLeaders': 'Points', 'ASTLeaders': 'Assists', 'STLLeaders': 'Steals', 
				'OREBLeaders': 'Offensive Rebounds', 'REBLeaders': 'Rebounds', 'BLKLeaders': 'Blocks', 'TOVLeaders': 'Turnovers',
				'FGMLeaders': 'Field Goals Made', 'FGALeaders': 'Field Goals Attempted', 'FG_PCTLeaders': 'Field Goals %', 
				'FG3MLeaders': 'Three Pointers Made', 'FG3ALeaders': 'Three Pointers Attempted', 'PFLeaders': 'Personal Fouls', 
				'FG3_PCTLeaders': 'Three Point %', 'FTMLeaders': 'Free Throws Made', 'FTALeaders': 'Free Throws Attempted', 
				'FT_PCTLeaders': 'Free Throws %', 'DREBLeaders': 'Defensive Rebounds' }
			limit = st.slider(label = 'How Many Players ?', min_value = 0, max_value = 1000, value = 5, step = 5)
			for _, dataset in enumerate( NBA_Alltime_Leaders( limit = limit )['resultSets'] ):
				st.write(f"** { headings[ dataset['name'] ] } Leaders **")
				data_frame = pandas.DataFrame( data = dataset['rowSet'], columns = dataset['headers'] )
				st.markdown( body = Excel_Downloader( df = data_frame ), unsafe_allow_html = True)
				st.dataframe( data = data_frame )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'NBA Team Yearly Stats':
		try:
			st.subheader('** NBA Team Yearly Stats **')
			League_Standings = NBA_League_Standings()['resultSets'][0]
			NBA_Teams = pandas.DataFrame( data = League_Standings['rowSet'], columns = League_Standings['headers'] )
			NBA_Teams['Team_Name'] = NBA_Teams['TeamCity'] + ' ' + NBA_Teams['TeamName']
			NBA_Teams = { tid : tname for tid, tname in zip( list(NBA_Teams.TeamID.unique()), list(NBA_Teams.Team_Name.unique()) ) }
			team_name = st.selectbox(label = 'Select NBA Team', options = list(NBA_Teams.values()) )
			for TEAM_ID, TEAM_NAME in NBA_Teams.items():
				if TEAM_NAME == team_name:
					data_dump = NBA_Team_YearByYear_Stats( team_id = TEAM_ID )['resultSets'][0]
					dataset = pandas.DataFrame( data = data_dump['rowSet'], columns = data_dump['headers'] )
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
					st.write(f'** { TEAM_NAME } - Championship Titles Count **')
					pivot_titles = pandas.pivot_table(dataset, index = 'NBA_FINALS_APPEARANCE', 
						values = 'TEAM_NAME', aggfunc = 'count', fill_value = 0)
					st.dataframe( data = pivot_titles )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')


#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#