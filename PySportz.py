__author__ = 'akashjeez'

import os, io, string, base64, pandas, requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as soup
import streamlit as st
from dateutil import parser
from fake_useragent import UserAgent

#---------------------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config(page_title = 'Py$p☢rtz', page_icon = '🏅', layout = 'wide', initial_sidebar_state = 'auto' )

st.title(body = 'Py$p☢rtz')

#---------------------------------------------------------------------------------------------------------------------------------#

## Reference => https://github.com/swar/nba_api, https://github.com/kashav/nba.js
## Reference => https://pypi.org/project/MLB-StatsAPI/
## Reference => http://static.nfl.com/liveupdate/scores/scores.json
## https://static.nfl.com/liveupdate/game-center/2020101600/2020101600_gtd.json
## https://static.nfl.com/ajax/scorestrip?season=2020&seasonType=REG&week=1

## NBA Team -> https://balldontlie.io/api/v1/teams

CATEGORIES: dict = {
	'Catalog': None,
	'MLB League': ('About MLB', 'MLB Alumnis', 'MLB Attendances', 'MLB DataCasters', 'MLB Divisions', 'MLB Drafts', 
		'MLB League Standings', 'MLB Leagues', 'MLB Players', 'MLB Schedule', 'MLB Sports', 'MLB Team Coaches', 
		'MLB Team Personnel', 'MLB Team Rosters', 'MLB Teams', 'MLB Umpires', 'MLB Venues', ),
	'NBA League': ('About NBA', 'NBA All Time Leaders', 'NBA Coaches', 'NBA League Players', 'NBA League Standings', 
		'NBA Player Profile', 'NBA Players', 'NBA ScoreBoard 1', 'NBA ScoreBoard 2', 'NBA Team Yearly Stats', 'NBA Teams', ),
	'NFL League': ('About NFL', 'NFL Player Stats', 'NFL Players', 'NFL Standings', 'NFL Team Stats', 'NFL Teams', ),
	'Cricket Stats': ('Cricket Stats', ),
	'Cricket IPL Stats': ('Best Batting Average', 'Best Bowling Average', 'Best Bowling Average Strike Rate', 
		'Best Bowling Average Strike Rate in Innings', 'Best Bowling Economy', 'Best Bowling in Innings', 'Best Strike Rate', 
		'Best Strike Rate in Innings', 'Fastest Centuries', 'Fastest Fifties', 'Highest Scores', 'IPL Winners', 'Most 4 Wickets', 
		'Most Centuries', 'Most Dot Balls', 'Most Fifties', 'Most Fours', 'Most Maiden Overs', 'Most Runs', 'Most Runs Conceded', 
		'Most Sixes', 'Most Sixes in Innings', 'Most Wickets', 'Points Table', ),
	'Cricket ICC Rankings': ('ODI Player All-Rounder Stats', 'ODI Player Batting Stats', 'ODI Player Bowling Stats', 'ODI Team Stats', 
		'T20I Player All-Rounder Stats', 'T20I Player Batting Stats', 'T20I Player Bowling Stats', 'T20I Team Stats', 
		'Test Player All-Rounder Stats', 'Test Player Batting Stats', 'Test Player Bowling Stats', 'Test Team Stats', ),
	'Cricket WC Stats': ('About Cricket World Cup', 'Best Batting Average', 'Best Batting Strike Rate', 
		'Best Batting Strike Rate Innings', 'Best Bowling Average', 'Best Bowling Economy', 'Best Bowling Economy Innings', 
		'Best Bowling Figures', 'Best Bowling Strike Rate', 'Best Bowling Strike Rate Innings', 'Best Win Percetage', 
		'Fastest Centuries', 'Fastest Fifties', 'Highest Match Aggregate', 'Highest Scores', 'ICC Cricket World Cup Winners', 
		'Largest Victories Runs', 'Largest Victories Wickets', 'Most Centuries', 'Most Dot Balls', 'Most Dot Balls Innings', 
		'Most Fifties', 'Most Fours', 'Most Losses', 'Most Maidens', 'Most Runs', 'Most Sixes', 'Most Wickets', 'Most Wins', ),
}

MLB_BASE_URL: str = 'https://statsapi.mlb.com'
NBA_BASE_URL: str = 'https://stats.nba.com'
NBA_BASE_URL_2: str = 'http://data.nba.net/data/prod'
NFL_BASE_URL: str = 'https://nfl.com'
IPL_BASE_URL: str = 'https://iplt20.com/stats'
ICC_BASE_URL: str = 'https://icc-cricket.com/rankings/mens'
ICC_CWC_BASE_URL: str = 'https://cricketworldcup.com/stats'
CRICKET_STATS_BASE_URL: str = 'https://stats.espncricinfo.com/ci/engine/records/{}'

## Static Headers for NBA League.
NBA_STATIC_HEADERS: dict = {
	'Host': 'stats.nba.com', 
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
	'Accept': 'application/json, text/plain, */*', 
	'Accept-Language': 'en-US,en;q=0.5', 
	'Accept-Encoding': 'gzip, deflate, br', 
	'x-nba-stats-origin': 'stats', 'x-nba-stats-token': 'true', 
	'Connection': 'keep-alive', 'Referer': NBA_BASE_URL, 
	'Pragma': 'no-cache', 'Cache-Control': 'no-cache'
}

## NBA Teams List.
NBA_TEAMS: list = [
	{'ID': 1610612737, 'Code': 'ATL', 'City': 'Atlanta', 'Conference': 'East', 'Division': 'Southeast', 'Team_Name': 'Atlanta Hawks'},
	{'ID': 1610612738, 'Code': 'BOS', 'City': 'Boston', 'Conference': 'East', 'Division': 'Atlantic', 'Team_Name': 'Boston Celtics'},
	{'ID': 1610612751, 'Code': 'BKN', 'City': 'Brooklyn', 'Conference': 'East', 'Division': 'Atlantic', 'Team_Name': 'Brooklyn Nets'},
	{'ID': 1610612766, 'Code': 'CHA', 'City': 'Charlotte', 'Conference': 'East', 'Division': 'Southeast', 'Team_Name': 'Charlotte Hornets'},
	{'ID': 1610612741, 'Code': 'CHI', 'City': 'Chicago', 'Conference': 'East', 'Division': 'Central', 'Team_Name': 'Chicago Bulls'},
	{'ID': 1610612739, 'Code': 'CLE', 'City': 'Cleveland', 'Conference': 'East', 'Division': 'Central', 'Team_Name': 'Cleveland Cavaliers'},
	{'ID': 1610612742, 'Code': 'DAL', 'City': 'Dallas', 'Conference': 'West', 'Division': 'Southwest', 'Team_Name': 'Dallas Mavericks'},
	{'ID': 1610612743, 'Code': 'DEN', 'City': 'Denver', 'Conference': 'West', 'Division': 'Northwest', 'Team_Name': 'Denver Nuggets'},
	{'ID': 1610612765, 'Code': 'DET', 'City': 'Detroit', 'Conference': 'East', 'Division': 'Central', 'Team_Name': 'Detroit Pistons'},
	{'ID': 1610612744, 'Code': 'GSW', 'City': 'Golden State', 'Conference': 'West', 'Division': 'Pacific', 'Team_Name': 'Golden State Warriors'},
	{'ID': 1610612745, 'Code': 'HOU', 'City': 'Houston', 'Conference': 'West', 'Division': 'Southwest', 'Team_Name': 'Houston Rockets'},
	{'ID': 1610612754, 'Code': 'IND', 'City': 'Indiana', 'Conference': 'East', 'Division': 'Central', 'Team_Name': 'Indiana Pacers'},
	{'ID': 1610612746, 'Code': 'LAC', 'City': 'Los Angeles', 'Conference': 'West', 'Division': 'Pacific', 'Team_Name': 'Los Angeles Clippers'},
	{'ID': 1610612747, 'Code': 'LAL', 'City': 'Los Angeles', 'Conference': 'West', 'Division': 'Pacific', 'Team_Name': 'Los Angeles Lakers'},
	{'ID': 1610612763, 'Code': 'MEM', 'City': 'Memphis', 'Conference': 'West', 'Division': 'Southwest', 'Team_Name': 'Memphis Grizzlies'},
	{'ID': 1610612748, 'Code': 'MIA', 'City': 'Miami', 'Conference': 'East', 'Division': 'Southeast', 'Team_Name': 'Miami Heat'},
	{'ID': 1610612749, 'Code': 'MIL', 'City': 'Milwaukee', 'Conference': 'East', 'Division': 'Central', 'Team_Name': 'Milwaukee Bucks'},
	{'ID': 1610612750, 'Code': 'MIN', 'City': 'Minnesota', 'Conference': 'West', 'Division': 'Northwest', 'Team_Name': 'Minnesota Timberwolves'},
	{'ID': 1610612740, 'Code': 'NOP', 'City': 'New Orleans', 'Conference': 'West', 'Division': 'Southwest', 'Team_Name': 'New Orleans Pelicans'},
	{'ID': 1610612752, 'Code': 'NYK', 'City': 'New York', 'Conference': 'East', 'Division': 'Atlantic', 'Team_Name': 'New York Knicks'},
	{'ID': 1610612760, 'Code': 'OKC', 'City': 'Oklahoma City', 'Conference': 'West', 'Division': 'Northwest', 'Team_Name': 'Oklahoma City Thunder'},
	{'ID': 1610612753, 'Code': 'ORL', 'City': 'Orlando', 'Conference': 'East', 'Division': 'Southeast', 'Team_Name': 'Orlando Magic'},
	{'ID': 1610612755, 'Code': 'PHI', 'City': 'Philadelphia', 'Conference': 'East', 'Division': 'Atlantic', 'Team_Name': 'Philadelphia 76ers'},
	{'ID': 1610612756, 'Code': 'PHX', 'City': 'Phoenix', 'Conference': 'West', 'Division': 'Pacific', 'Team_Name': 'Phoenix Suns'},
	{'ID': 1610612757, 'Code': 'POR', 'City': 'Portland', 'Conference': 'West', 'Division': 'Northwest', 'Team_Name': 'Portland Trail Blazers'},
	{'ID': 1610612758, 'Code': 'SAC', 'City': 'Sacramento', 'Conference': 'West', 'Division': 'Pacific', 'Team_Name': 'Sacramento Kings'},
	{'ID': 1610612759, 'Code': 'SAS', 'City': 'San Antonio', 'Conference': 'West', 'Division': 'Southwest', 'Team_Name': 'San Antonio Spurs'},
	{'ID': 1610612761, 'Code': 'TOR', 'City': 'Toronto', 'Conference': 'East', 'Division': 'Atlantic', 'Team_Name': 'Toronto Raptors'},
	{'ID': 1610612762, 'Code': 'UTA', 'City': 'Utah', 'Conference': 'West', 'Division': 'Northwest', 'Team_Name': 'Utah Jazz'},
	{'ID': 1610612764, 'Code': 'WAS', 'City': 'Washington', 'Conference': 'East', 'Division': 'Southeast', 'Team_Name': 'Washington Wizards'},
]

## NFL Teams List.
NFL_TEAMS: list = [
	{'Team_Name': 'Arizona Cardinals', 'Active_Since': 1920, 'Conference': 'National Football Conference', 'Division': 'NFC West'},
	{'Team_Name': 'Atlanta Falcons', 'Active_Since': 1966, 'Conference': 'National Football Conference', 'Division': 'NFC South'},
	{'Team_Name': 'Baltimore Ravens', 'Active_Since': 1996, 'Conference': 'American Football Conference', 'Division': 'AFC North'},
	{'Team_Name': 'Buffalo Bills', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC East'},
	{'Team_Name': 'Carolina Panthers', 'Active_Since': 1995, 'Conference': 'National Football Conference', 'Division': 'NFC South'},
	{'Team_Name': 'Chicago Bears', 'Active_Since': 1920, 'Conference': 'National Football Conference', 'Division': 'NFC North'},
	{'Team_Name': 'Cincinnati Bengals', 'Active_Since': 1968, 'Conference': 'American Football Conference', 'Division': 'AFC North'},
	{'Team_Name': 'Cleveland Browns', 'Active_Since': 1950, 'Conference': 'American Football Conference', 'Division': 'AFC North'},
	{'Team_Name': 'Dallas Cowboys', 'Active_Since': 1960, 'Conference': 'National Football Conference', 'Division': 'NFC East'},
	{'Team_Name': 'Denver Broncos', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC West'},
	{'Team_Name': 'Detroit Lions', 'Active_Since': 1930, 'Conference': 'National Football Conference', 'Division': 'NFC North'},
	{'Team_Name': 'Green Bay Packers', 'Active_Since': 1921, 'Conference': 'National Football Conference', 'Division': 'NFC North'},
	{'Team_Name': 'Houston Texans', 'Active_Since': 2002, 'Conference': 'American Football Conference', 'Division': 'AFC South'},
	{'Team_Name': 'Indianapolis Colts', 'Active_Since': 1953, 'Conference': 'American Football Conference', 'Division': 'AFC South'},
	{'Team_Name': 'Jacksonville Jaguars', 'Active_Since': 1995, 'Conference': 'American Football Conference', 'Division': 'AFC South'},
	{'Team_Name': 'Kansas City Chiefs', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC West'},
	{'Team_Name': 'Las Vegas Raiders', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC West'},
	{'Team_Name': 'Los Angeles Chargers', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC West'},
	{'Team_Name': 'Los Angeles Rams', 'Active_Since': 1937, 'Conference': 'National Football Conference', 'Division': 'NFC West'},
	{'Team_Name': 'Miami Dolphins', 'Active_Since': 1966, 'Conference': 'American Football Conference', 'Division': 'AFC East'},
	{'Team_Name': 'Minnesota Vikings', 'Active_Since': 1961, 'Conference': 'National Football Conference', 'Division': 'NFC North'},
	{'Team_Name': 'New England Patriots', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC East'},
	{'Team_Name': 'New Orleans Saints', 'Active_Since': 1967, 'Conference': 'National Football Conference', 'Division': 'NFC South'},
	{'Team_Name': 'New York Giants', 'Active_Since': 1925, 'Conference': 'National Football Conference', 'Division': 'NFC East'},
	{'Team_Name': 'New York Jets', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC East'},
	{'Team_Name': 'Philadelphia Eagles', 'Active_Since': 1933, 'Conference': 'National Football Conference', 'Division': 'NFC East'},
	{'Team_Name': 'Pittsburgh Steelers', 'Active_Since': 1933, 'Conference': 'American Football Conference', 'Division': 'AFC North'},
	{'Team_Name': 'San Francisco 49ers', 'Active_Since': 1950, 'Conference': 'National Football Conference', 'Division': 'NFC West'},
	{'Team_Name': 'Seattle Seahawks', 'Active_Since': 1976, 'Conference': 'National Football Conference', 'Division': 'NFC West'},
	{'Team_Name': 'Tampa Bay Buccaneers', 'Active_Since': 1976, 'Conference': 'National Football Conference', 'Division': 'NFC South'},
	{'Team_Name': 'Tennessee Titans', 'Active_Since': 1960, 'Conference': 'American Football Conference', 'Division': 'AFC South'},
	{'Team_Name': 'Washington Football Team', 'Active_Since': 1932, 'Conference': 'National Football Conference', 'Division': 'NFC East'}
]

## Cricket IPL Teams List
IPL_TEAMS: list = [
	{'Team_name': 'Chennai Super Kings', 'City': 'Chennai, Tamil Nadu', 'Home_Ground': 'M. A. Chidambaram Stadium'},
	{'Team_name': 'Delhi Capitals', 'City': 'Delhi, NCR', 'Home_Ground': 'Arun Jaitley Stadium'},
	{'Team_name': 'Kings XI Punjab', 'City': 'Mohali, Punjab', 'Home_Ground': 'PCA Stadium'},
	{'Team_name': 'Kolkata Knight Riders', 'City': 'Kolkata, West Bengal', 'Home_Ground': 'Eden Gardens'},
	{'Team_name': 'Mumbai Indians', 'City': 'Mumbai, Maharashtra', 'Home_Ground': 'Wankhede Stadium'},
	{'Team_name': 'Rajastan Royals', 'City': 'Jaipur, Rajasthan', 'Home_Ground': 'Sawai Mansingh Stadium'},
	{'Team_name': 'Royal Challengers Bangalore', 'City': 'Bengaluru, Karnataka', 'Home_Ground': 'M. Chinnaswamy Stadium'},
	{'Team_name': 'Sunrisers Hyderabad', 'City': 'Hyderabad, Telangana', 'Home_Ground': 'Rajiv Gandhi International Cricket Stadium'},
]

#---------------------------------------------------------------------------------------------------------------------------------#

def Excel_Downloader(df: pandas.DataFrame) -> str:
	output = io.BytesIO()
	writer = pandas.ExcelWriter(path = output, engine = 'xlsxwriter')
	df.to_excel(excel_writer = writer, sheet_name = 'Data', index = False)
	writer.save()
	processed_data = output.getvalue()
	b64 = base64.b64encode(processed_data)
	return f"<a href = 'data:application/octet-stream;base64,{b64.decode()}' download = 'Data.xlsx'> Download Excel </a>"


@st.cache
def Cricket_Stats() -> pandas.DataFrame:
	dataset, URLS = [], {
		'MENS_TEST': CRICKET_STATS_BASE_URL.format('index.html?class=1'),
		'MENS_ODI': CRICKET_STATS_BASE_URL.format('index.html?class=2'),
		'MENS_T20I': CRICKET_STATS_BASE_URL.format('index.html?class=3'),
		'MENS_FIRST_CLASS': CRICKET_STATS_BASE_URL.format('index.html?class=4'),
		'MENS_LIST_A_MATCHES': CRICKET_STATS_BASE_URL.format('index.html?class=5'),
		'MENS_T20': CRICKET_STATS_BASE_URL.format('index.html?class=6'),
		'WOMENS_TEST': CRICKET_STATS_BASE_URL.format('index.html?class=8'),
		'WOMENS_ODI': CRICKET_STATS_BASE_URL.format('index.html?class=9'),
		'WOMENS_T20I': CRICKET_STATS_BASE_URL.format('index.html?class=10'),
		'MENS_COMBINED_ALL': CRICKET_STATS_BASE_URL.format('index.html?class=11'),
	}
	for category_name, category_link in URLS.items():
		page = soup(requests.get( category_link ).text, 'lxml')
		for data in page.find_all('a', class_ = 'RecordLinks'):
			sub_category_name = data.text.strip().replace('(', '').replace(')', '').replace(' ', '_').upper()
			sub_category_id = data.get('href').strip().split('/')[-1].split('.')[0]
			if sub_category_id.isdigit():
				dataset.append({ 
					'category': category_name, 
					'sub_category': sub_category_name, 
					'sub_category_id': sub_category_id 
				})
	return pandas.DataFrame( data = dataset )


@st.cache
def List_MLB_Teams() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/teams').json()
		for data in response['teams']:
			data_dump = {
				'Team_ID': data.get('id', 'TBD'),
				'Team_Name': data.get('name', 'TBD').upper(),
				'Team_Code': data.get('teamCode', 'TBD').upper(),
				'Abbreviation': data.get('abbreviation', 'TBD'),
				'Team_Short_Name': data.get('shortName', 'TBD').upper(),
				'Location': data.get('locationName', 'TBD').upper(),
				'First_Year_Of_Play': data.get('firstYearOfPlay', 'TBD'),
				'Team_Link': f"{ MLB_BASE_URL }{ data.get('link', 'TBD') }",
				'Season': data.get('season', 'TBD'),
				'All_Star_Status': data.get('allStarStatus', 'TBD'),
				'Team_Active': 'TBD' if 'active' not in data.keys() else 'Yes' 
					if data.get('active') == True else 'No', 
				'Parent_Org_ID': data.get('parentOrgId', 'TBD'),
				'Parent_Org_Name': data.get('parentOrgName', 'TBD')
			}
			if 'league' in data.keys():
				data_dump.update({
					'League_ID': data.get('league').get('id', 'TBD'),
					'League_Name': data.get('league').get('name', 'TBD'),
					'League_Link': f"{ MLB_BASE_URL }{ data.get('league').get('link', 'TBD') }",
				})
			if 'venue' in data.keys():
				data_dump.update({
					'Venue_ID': data.get('venue').get('id', 'TBD'),
					'Venue_Name': data.get('venue').get('name', 'TBD'),
					'Venue_Link': f"{ MLB_BASE_URL }{ data.get('venue').get('link', 'TBD') }",
				})
			if 'division' in data.keys():
				data_dump.update({
					'Division_ID': data.get('division').get('id', 'TBD'),
					'Division_Name': data.get('division').get('name', 'TBD'),
					'Division_Link': f"{ MLB_BASE_URL }{ data.get('division').get('link', 'TBD') }",
				})
			if 'sport' in data.keys():
				data_dump.update({
					'Sport_ID': data.get('sport').get('id', 'TBD'),
					'Sport_Name': data.get('sport').get('name', 'TBD'),
					'Sport_Link': f"{ MLB_BASE_URL }{ data.get('sport').get('link', 'TBD') }",	
				})
			if 'springLeague' in data.keys():
				data_dump.update({
					'Spring_League_ID': data.get('springLeague').get('id', 'TBD'),
					'Spring_League_Name': data.get('springLeague').get('name', 'TBD'),
					'Spring_League_Link': f"{ MLB_BASE_URL }{ data.get('springLeague').get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Sports() -> dict:
	try:
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/sports').json()
		dataset: list = [{
			'Sport_ID': data.get('id', 'TBD'),
			'Sport_Name': data.get('name', 'TBD'),
			'Sport_Code': data.get('code', 'TBD').upper(),
			'Abbreviation': data.get('abbreviation', 'TBD'),
			'Sport_Active': 'TBD' if 'activeStatus' not in data.keys() else 'Yes' 
				if data.get('activeStatus') == True else 'No', 
		} for data in response['sports'] ]
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Players(sport_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/sports/{sport_id}/players').json()
		for data in response.get('people'):
			data_dump: dict = {
				'Player_ID': data.get('id', 'TBD'),
				'Player_First_Name': data.get('firstName', 'TBD').upper(),
				'Player_Last_Name': data.get('lastName', 'TBD').upper(),
				'Player_Name': data.get('fullName', 'TBD').upper(),
				'Player_Full_Name': data.get('fullFMLName', 'TBD').upper(),
				'Jersey_Number': data.get('primaryNumber', 'TBD'),
				'Date_Of_Birth': parser.parse( data['birthDate'] ).strftime('%d-%m-%Y') 
					if 'birthDate' in data.keys() else 'TBD',
				'Current_Age': data.get('currentAge', 'TBD'),
				'Birth_City': data.get('birthCity', 'TBD'),
				'Birth_Country': data.get('birthCountry', 'TBD'),
				'Height': data.get('height', 'TBD'),
				'Weight': data.get('weight', 'TBD'),
				'Player_Active': 'TBD' if 'active' not in data.keys() else 'Yes' 
					if data.get('active') == True else 'No', 
				'Player_Name_Slug': data.get('nameSlug', 'TBD'),
				'Box_Score_Name': data.get('boxscoreName', 'TBD'),
				'Player_Gender': 'TBD' if 'gender' not in data.keys() else 'Male' 
					if data.get('gender') == 'M' else 'Female',
				'MLB_Debut_Date': parser.parse( data['mlbDebutDate'] ).strftime('%d-%m-%Y') 
					if 'mlbDebutDate' in data.keys() else 'TBD',
				'Strike_Zone_Top': data.get('strikeZoneTop', 'TBD'),
				'Strike_Zone_Bottom': data.get('strikeZoneBottom', 'TBD'),
			}
			if 'currentTeam' in data.keys():
				data_dump.update({
					'Current_Team_ID': data.get('currentTeam').get('id', 'TBD'),
					'Current_Team_Link': f"{ MLB_BASE_URL }{ data.get('currentTeam').get('link', 'TBD') }",	
				})
			if 'primaryPosition' in data.keys():
				data_dump.update({
					'Position_Code': data.get('primaryPosition').get('code', 'TBD'),
					'Position_Name': data.get('primaryPosition').get('name', 'TBD'),
					'Position_Type': data.get('primaryPosition').get('type', 'TBD'),
					'Position_Abbreviation': data.get('primaryPosition').get('abbreviation', 'TBD'),	
				})
			if 'batSide' in data.keys():
				data_dump.update({
					'Bat_Side_Code': data.get('batSide').get('code', 'TBD'),
					'Bat_Side_Description': data.get('batSide').get('description', 'TBD'),
				})
			if 'pitchHand' in data.keys():
				data_dump.update({
					'Pitch_Hand_Code': data.get('pitchHand').get('code', 'TBD'),
					'Pitch_Hand_Description': data.get('pitchHand').get('description', 'TBD'),
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Leagues() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/league').json()
		for data in response.get('leagues'):
			data_dump: dict = {
				'League_ID': data.get('id', 'TBD'),
				'League_Name': data.get('name', 'TBD'),
				'League_Link': f"{ MLB_BASE_URL }{ data.get('link', 'TBD') }",
				'Abbreviation': data.get('abbreviation', 'TBD'),
				'Season': data.get('season', 'TBD'),
				'Season_State': data.get('seasonState', 'TBD'),
				'Num_of_Games': data.get('numGames', 'TBD'),
				'Num_of_Teams': data.get('numTeams', 'TBD'),
			}
			if 'seasonDateInfo' in data.keys():
				data_dump.update({
					'Regular_Season_Start_Sate': parser.parse( data['seasonDateInfo']['regularSeasonStartDate'] ).strftime('%d-%m-%Y') 
						if 'regularSeasonStartDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Regular_Deason_End_Date': parser.parse( data['seasonDateInfo']['regularSeasonEndDate'] ).strftime('%d-%m-%Y') 
						if 'regularSeasonEndDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Pre_Season_Start_Date': parser.parse( data['seasonDateInfo']['preSeasonStartDate'] ).strftime('%d-%m-%Y') 
						if 'preSeasonStartDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Pre_Season_End_Date': parser.parse( data['seasonDateInfo']['preSeasonEndDate'] ).strftime('%d-%m-%Y') 
						if 'preSeasonEndDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Post_Season_Start_Date': parser.parse( data['seasonDateInfo']['postSeasonStartDate'] ).strftime('%d-%m-%Y') 
						if 'postSeasonStartDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Post_Season_End_Date': parser.parse( data['seasonDateInfo']['postSeasonEndDate'] ).strftime('%d-%m-%Y') 
						if 'postSeasonEndDate' in data.get('seasonDateInfo').keys() else 'TBD',
					'Last_Date_1st_Half': parser.parse( data['seasonDateInfo']['lastDate1stHalf'] ).strftime('%d-%m-%Y') 
						if 'lastDate1stHalf' in data.get('seasonDateInfo').keys() else 'TBD',
					'First_Date_2nd_Half': parser.parse( data['seasonDateInfo']['firstDate2ndHalf'] ).strftime('%d-%m-%Y') 
						if 'firstDate2ndHalf' in data.get('seasonDateInfo').keys() else 'TBD',
					'All_Star_Date': parser.parse( data['seasonDateInfo']['allStarDate'] ).strftime('%d-%m-%Y') 
						if 'allStarDate' in data.get('seasonDateInfo').keys() else 'TBD',
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Divisions() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/divisions').json()
		for data in response.get('divisions'):
			data_dump: dict = {
				'Division_ID': data.get('id', 'TBD'),
				'Division_Name': data.get('name', 'TBD').upper(),
				'Division_Short_Name': data.get('nameShort', 'TBD').upper(),
				'Abbreviation': data.get('abbreviation', 'TBD'),
				'Division_Link': f"{ MLB_BASE_URL }{ data.get('link', 'TBD') }",
				'Has_Wild_Card': 'TBD' if 'hasWildcard' not in data.keys() else 'Yes' 
					if data.get('hasWildcard') == True else 'No',
				'Playoff_Teams': data.get('numPlayoffTeams', 'TBD')
			}
			if 'league' in data.keys():
				data_dump.update({
					'League_ID': data.get('league').get('id', 'TBD'),
					'League_Link': f"{ MLB_BASE_URL }{ data.get('league').get('link', 'TBD') }",
				})
			if 'sport' in data.keys():
				data_dump.update({
					'Sport_ID': data.get('sport').get('id', 'TBD'),
					'Sport_Link': f"{ MLB_BASE_URL }{ data.get('sport').get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Schedule(sport_id: int = None, start_date: str = None, end_date: str = None) -> dict:
	try:
		dataset: str = []
		sport_id: int = int(sport_id) if sport_id is not None else 1
		request_url: str = f'{MLB_BASE_URL}/api/v1/schedule?sportId={sport_id}&startDate={start_date}&endDate={end_date}'
		response: dict = requests.get( url = request_url ).json()
		for day in response.get('dates'):
			for data in day.get('games'):
				data_dump: dict = {
					'Game_Date': parser.parse( day['date'] ).strftime('%d-%m-%Y') 
						if 'date' in day.keys() else 'TBD',
					'Total_Games': day.get('totalGames', 'TBD'),
					'Game_ID': data.get('gamePk', 'TBD'),
					'Game_Link': f"{ MLB_BASE_URL }{ data.get('link', 'TBD') }",
					'Game_Type': data.get('gameType', 'TBD'),
					'Season': data.get('season', 'TBD'),
					'Game_Datetime': datetime.strptime(data['gameDate'], '%Y-%m-%dT%H:%M:%SZ').\
						strftime('%d-%m-%Y %I:%M %p') if 'gameDate' in data.keys() else 'TBD',
					'Game_Tied': 'TBD' if 'isTie' not in data.keys() else 'Yes' 
						if data.get('isTie') == True else 'No',
					'Game_Number': data.get('gameNumber', 'TBD'),
					'Tie_Breaker': data.get('tiebreaker', 'TBD'),
					'Day_Night': data.get('dayNight', 'TBD').upper(),
					'Description': data.get('description', 'TBD'),
					'Scheduled_Innings': data.get('scheduledInnings', 'TBD'),
					'Games_In_Series': data.get('gamesInSeries', 'TBD'),
					'Series_Game_Number': data.get('seriesGameNumber', 'TBD'),
					'Series_Description': data.get('seriesDescription', 'TBD')
				}
				if 'content' in data.keys():
					data_dump.update({
						'Content_Link': f"{ MLB_BASE_URL }{ data.get('content').get('link', 'TBD') }",
					})
				if 'venue' in data.keys():
					data_dump.update({
						'Venue_ID': data.get('venue').get('id', 'TBD'),
						'Venue_Name': data.get('venue').get('name', 'TBD'),
						'Venue_Link': f"{ MLB_BASE_URL }{ data.get('venue').get('link', 'TBD') }",
					})
				if 'status' in data.keys():
					data_dump.update({
						'Abstract_Game_State': data.get('status').get('abstractGameState', 'TBD'),
						'Detailed_State': data.get('status').get('detailedState', 'TBD'),
					})
				if 'teams' in data.keys():
					if 'away' in data['teams'].keys():
						data_dump.update({
							'Away_Team_Score': data['teams']['away'].get('score', 'TBD'),
							'Away_Team_Winner': 'TBD' if 'isWinner' not in data['teams']['away'].keys() else
								'Yes' if data['teams']['away'].get('isWinner') == True else 'No',
							'Away_Team_Series_Num': data['teams']['away'].get('seriesNumber', 'TBD'),
						})
						if 'leagueRecord' in data['teams']['away'].keys():
							data_dump.update({
								'Away_Team_League_Wins': data['teams']['away']['leagueRecord'].get('wins', 'TBD'),
								'Away_Team_League_Loss': data['teams']['away']['leagueRecord'].get('losses', 'TBD'),
								'Away_Team_League_Pct': data['teams']['away']['leagueRecord'].get('pct', 'TBD'),
							})
						if 'streak' in data['teams']['away'].keys():
							data_dump.update({
								'Away_Team_ID': data['teams']['away']['team'].get('id', 'TBD'),
								'Away_Team_Name': data['teams']['away']['team'].get('name', 'TBD'),
								'Away_Team_Link': f"{ MLB_BASE_URL } { data['teams']['away']['team'].get('link', 'TBD') }",
							})
					if 'home' in data['teams'].keys():
						data_dump.update({
							'Home_Team_Score': data['teams']['home'].get('score', 'TBD'),
							'Home_Team_Winner': 'TBD' if 'isWinner' not in data['teams']['home'].keys() else
								'Yes' if data['teams']['home'].get('isWinner') == True else 'No',
							'Home_Team_Series_Num': data['teams']['home'].get('seriesNumber', 'TBD'),
						})
						if 'leagueRecord' in data['teams']['home'].keys():
							data_dump.update({
								'Home_Team_League_Wins': data['teams']['home']['leagueRecord'].get('wins', 'TBD'),
								'Home_Team_League_Loss': data['teams']['home']['leagueRecord'].get('losses', 'TBD'),
								'Home_Team_League_Pct': data['teams']['home']['leagueRecord'].get('pct', 'TBD'),
							})
						if 'team' in data['teams']['home'].keys():
							data_dump.update({
								'Home_Team_ID': data['teams']['home']['team'].get('id', 'TBD'),
								'Home_Team_Name': data['teams']['home']['team'].get('name', 'TBD'),
								'Home_Team_Link': f"{ MLB_BASE_URL } { data['teams']['home']['team'].get('link', 'TBD') }",
							})
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Rosters(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/teams/{team_id}/roster').json()
		for data in response.get('roster'):
			data_dump: dict = {
				'Team_id': team_id,
				'Jersey_Number': data.get('jerseyNumber', 'TBD'),
				'Position': data.get('position', 'TBD').get('name', 'TBD'),
				'Status': data.get('status', 'TBD').get('description', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Player_Name': data['person'].get('fullName', 'TBD'),
					'Player_Link': f"{ MLB_BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Personnel(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/teams/{team_id}/personnel').json()
		for data in response.get('roster'):
			data_dump: dict = {
				'Team_ID': team_id,
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Player_Name': data['person'].get('fullName', 'TBD'),
					'Player_Link': f"{ MLB_BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Coaches(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/teams/{team_id}/coaches').json()
		for data in response.get('roster'):
			data_dump: dict = {
				'Team_ID': team_id,
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ MLB_BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Attendances(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/attendance?teamId={team_id}').json()
		for data in response.get('records'):
			data_dump: dict = {
				'Total_Openings': data.get('openingsTotal', 'TBD'),
				'Total_Away_Openings': data.get('openingsTotalAway', 'TBD'),
				'Total_Home_Openings': data.get('openingsTotalHome', 'TBD'),
				'Total_Lost_Openings': data.get('openingsTotalLost', 'TBD'),
				'Total_YTD_Openings': data.get('openingsTotalYtd', 'TBD'),
				'Total_Games': data.get('gamesTotal', 'TBD'), 'Year': data.get('year', 'TBD'),
				'Total_Away_Games': data.get('gamesAwayTotal', 'TBD'),
				'Total_Home_Games': data.get('gamesHomeTotal', 'TBD'),
				'Avg_Away_Attendance': data.get('attendanceAverageAway', 'TBD'),
				'Avg_Home_Attendance': data.get('attendanceAverageHome', 'TBD'),
				'Avg_YTD_Attendance': data.get('attendanceAverageYtd', 'TBD'),
				'Total_Attendance': data.get('attendanceTotal', 'TBD'),
				'Total_Away_Attendance': data.get('attendanceTotalAway', 'TBD'),
				'Total_Home_Attendance': data.get('attendanceTotalHome', 'TBD'),
				'Total_YTD_Attendance': data.get('attendanceTotalYtd', 'TBD'),
				'High_Attendance': data.get('attendanceHigh', 'TBD'),
				'High_Attendance_Date': data.get('attendanceHighDate', 'TBD'),
				'Low_Attendance': data.get('attendanceLow', 'TBD'),
				'Low_Attendance_Date': data.get('attendanceLowDate', 'TBD'),
			}
			if 'gameType' in data.keys():
				data_dump.update({
					'Game_Type': data['gameType'].get('description', 'TBD')
				})
			if 'team' in data.keys():
				data_dump.update({
					'Team_ID': data['team'].get('id', 'TBD'),
					'Team_Name': data['team'].get('name', 'TBD'),
					'Team_Link': f"{ MLB_BASE_URL }{ data['team'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Venues() -> dict:
	try:
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/venues').json()
		dataset: list = [{
			'Venue_ID': data.get('id', 'TBD'),
			'Venue_Name': data.get('name', 'TBD'),
			'Venue_Link': f"{ MLB_BASE_URL }{ data.get('link', 'TBD') }",
		} for data in response.get('venues') ]
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Alumnis(team_id: int) -> dict:
	try:
		dataset, season = [], datetime.now().year
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/teams/{team_id}/alumni?season={season}').json()
		for data in response.get('people'):
			data_dump: dict = {
				'Player_ID': data.get('id', 'TBD'),
				'Player_First_Name': data.get('firstName', 'TBD').upper(),
				'Player_Last_Name': data.get('lastName', 'TBD').upper(),
				'Player_Name': data.get('fullName', 'TBD').upper(),
				'Player_Full_Name': data.get('fullFMLName', 'TBD').upper(),
				'Jersey_Number': data.get('primaryNumber', 'TBD'),
				'Date_Of_Birth': parser.parse( data['birthDate'] ).strftime('%d-%m-%Y') 
					if 'birthDate' in data.keys() else 'TBD',
				'Current_Age': data.get('currentAge', 'TBD'),
				'Birth_City': data.get('birthCity', 'TBD'), 'Draft_Year': data.get('draftYear', 'TBD'),
				'Birth_Country': data.get('birthCountry', 'TBD'),
				'Height': data.get('height', 'TBD'), 'Weight': data.get('weight', 'TBD'),
				'Player_Active': 'TBD' if 'isPlayer' not in data.keys() else 'Yes' 
					if data.get('isPlayer') == True else 'No', 
				'Player_Name_Slug': data.get('nameSlug', 'TBD'),
				'Box_Score_Name': data.get('boxscoreName', 'TBD'),
				'Player_Gender': 'TBD' if 'gender' not in data.keys() else 'Male' 
					if data.get('gender') == 'M' else 'Female',
				'MLB_Debut_Date': parser.parse( data['mlbDebutDate'] ).strftime('%d-%m-%Y') 
					if 'mlbDebutDate' in data.keys() else 'TBD',
				'Strike_Zone_Top': data.get('strikeZoneTop', 'TBD'),
				'Strike_Zone_Bottom': data.get('strikeZoneBottom', 'TBD'),
				'Alumni_Last_Season': data.get('alumniLastSeason', 'TBD'),
			}
			if 'primaryPosition' in data.keys():
				data_dump.update({
					'Position_Code': data.get('primaryPosition').get('code', 'TBD'),
					'Position_Name': data.get('primaryPosition').get('name', 'TBD'),
					'Position_Type': data.get('primaryPosition').get('type', 'TBD'),
					'Position_Abbreviation': data.get('primaryPosition').get('abbreviation', 'TBD'),	
				})
			if 'batSide' in data.keys():
				data_dump.update({
					'Bat_Side_Code': data['batSide'].get('code', 'TBD'),
					'Bat_Side_Description': data['batSide'].get('description', 'TBD'),
				})
			if 'pitchHand' in data.keys():
				data_dump.update({
					'Pitch_Hand_Code': data['pitchHand'].get('code', 'TBD'),
					'Pitch_Hand_Description': data['pitchHand'].get('description', 'TBD'),
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_League_Standings(league_id: str) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/standings?leagueId={league_id}').json()
		for record in response.get('records'):
			for data in record.get('teamRecords'):
				data_dump: dict = {
					'Standing_Type': record.get('standingsType', 'TBD'),
					'Last_Updated': record.get('lastUpdated', 'TBD'),
					'Season': data.get('season', 'TBD'),
					'Wins': data.get('wins', 'TBD'), 'Losses': data.get('losses', 'TBD'),
					'Clinch_Indicator': data.get('clinchIndicator', 'TBD'),
					'Division_Rank': data.get('divisionRank', 'TBD'),
					'League_Rank': data.get('leagueRank', 'TBD'),
					'Sport_Rank': data.get('sportRank', 'TBD'),
					'Games_Played': data.get('gamesPlayed', 'TBD'),
					'Games_Back': data.get('gamesBack', 'TBD'),
					'Runs_Allowed': data.get('runsAllowed', 'TBD'),
					'Runs_Scored': data.get('runsScored', 'TBD'),
					'Division_Champ': 'TBD' if 'divisionChamp' not in data.keys() else 'Yes'
						if data['divisionChamp'] == True else 'No',
					'Division_Leader': 'TBD' if 'divisionLeader' not in data.keys() else 'Yes'
						if data['divisionLeader'] == True else 'No',
					'Has_Wild_Card': 'TBD' if 'hasWildcard' not in data.keys() else 'Yes'
						if data['hasWildcard'] == True else 'No',
					'Clinched': 'TBD' if 'clinched' not in data.keys() else 'Yes'
						if data['clinched'] == True else 'No',
					'Elimination_Number': data.get('eliminationNumber', 'TBD'),
					'Wildcard_Elimination_Number': data.get('wildCardEliminationNumber', 'TBD'),
					'Wildcard_Games_Back': data.get('wildCardGamesBack', 'TBD'),
					'League_Games_Back': data.get('leagueGamesBack', 'TBD'),
					'Spring_League_Games_Back': data.get('springLeagueGamesBack', 'TBD'),
					'Sport_Games_Back': data.get('sportGamesBack', 'TBD'),
					'Division_Games_Back': data.get('divisionGamesBack', 'TBD'),
					'Conference_Games_Back': data.get('conferenceGamesBack', 'TBD'),
					'Run_Differential': data.get('runDifferential', 'TBD'),
					'Winning_Percentage': data.get('winningPercentage', 'TBD')
				}
				if 'team' in data.keys():
					data_dump.update({
						'Team_ID': data['team'].get('id', 'TBD'),
						'Team_Name': data['team'].get('name', 'TBD'),
						'Team_Link': f"{ MLB_BASE_URL }{ data['team'].get('link', 'TBD') }",
					})
				if 'streak' in data.keys():
					data_dump.update({
						'Streak_Type': data['streak'].get('streakType', 'TBD'),
						'Streak_Number': data['streak'].get('streakNumber', 'TBD'),
						'Streak_Code': data['streak'].get('streakCode', 'TBD'),
					})
				if 'leagueRecord' in data.keys():
					data_dump.update({
						'League_Wins': data['leagueRecord'].get('wins', 'TBD'),
						'League_Losses': data['leagueRecord'].get('losses', 'TBD'),
						'League_PCT': data['leagueRecord'].get('pct', 'TBD'),
					})
				if 'records' in data.keys():
					if 'splitRecords' in data['records'].keys():
						data_dump.update( { 'Split_Records': data['records']['splitRecords'] } )
					if 'divisionRecords' in data['records'].keys():
						data_dump.update( { 'Division_Records': data['records']['divisionRecords'] } )
					if 'overallRecords' in data['records'].keys():
						data_dump.update( { 'Overall_Records': data['records']['overallRecords'] } )
					if 'leagueRecords' in data['records'].keys():
						data_dump.update( { 'League_Records': data['records']['leagueRecords'] } )
					if 'expectedRecords' in data['records'].keys():
						data_dump.update( { 'Expected_Records': data['records']['expectedRecords'] } )
				if 'league' in record.keys():
					data_dump.update({
						'League_ID': record['league'].get('id', 'TBD'),
						'League_Link': f"{ MLB_BASE_URL }{ record['league'].get('link', 'TBD') }",
					})
				if 'sport' in record.keys():
					data_dump.update({
						'Sport_ID': record['sport'].get('id', 'TBD'),
						'Sport_Link': f"{ MLB_BASE_URL }{ record['sport'].get('link', 'TBD') }",
					})
				if 'division' in record.keys():
					data_dump.update({
						'Division_ID': record['division'].get('id', 'TBD'),
						'Division_Link': f"{ MLB_BASE_URL }{ record['division'].get('link', 'TBD') }",
					})
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Drafts() -> dict:
	try:
		dataset, year = [], datetime.now().year
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/draft/{year}').json()
		for rounds in response['drafts']['rounds']:
			for data in rounds.get('picks'):
				data_dump: dict = {
					'BIS_Player_ID': data.get('bisPlayerId', 'TBD'),
					'Pick_Round': data.get('pickRound', 'TBD'), 
					'Pick_Number': data.get('pickNumber', 'TBD'),
					'Rank': data.get('rank', 'TBD'), 
					'Blurb': data.get('blurb', 'TBD'),
					'Pick_Value': data.get('pickValue', 'TBD'),
					'Signing_Bonus': data.get('signingBonus', 'TBD'),
					'Player_Image': data.get('headshotLink', 'TBD'),
					'Scouting_Report': data.get('scoutingReport', 'TBD'),
					'Is_Draft': 'TBD' if 'isDrafted' not in data.keys() else
						'Yes' if data['isDrafted'] == True else 'No',
					'Is_Pass': 'TBD' if 'isPass' not in data.keys() else
						'Yes' if data['isPass'] == True else 'NO',
				}
				if 'person' in data.keys():
					data_dump.update({
						'Player_ID': data['person'].get('id', 'TBD'),
						'Player_First_Name': data['person'].get('firstName', 'TBD'),
						'Player_Last_Name': data['person'].get('lastName', 'TBD'),
						'Player_Full_Name': data['person'].get('fullFMLName', 'TBD'),
						'Primary_Number': data['person'].get('primaryNumber', 'TBD'),
						'Name_Slug': data['person'].get('nameSlug', 'TBD'),
						'Birth_Date': data['person'].get('birthDate', 'TBD'),
						'Current_Age': data['person'].get('currentAge', 'TBD'),
						'Birth_City': data['person'].get('birthCity', 'TBD'),
						'Birth_State': data['person'].get('birthStateProvince', 'TBD'),
						'Birth_Country': data['person'].get('birthCountry', 'TBD'),
						'Height': data['person'].get('height', 'TBD'),
						'Weight': data['person'].get('weight', 'TBD'),
						'Draft_Year': data['person'].get('draftYear', 'TBD'),
						'Is_Player': 'TBD' if 'isPlayer' not in data['person'].keys() \
							else 'Yes' if data['person']['isPlayer'] == True else 'No',
						'Gender': 'TBD' if 'gender' not in data['person'].keys() \
							else 'Male' if data['person']['gender'] == 'M' else 'Female',
						'Strike_Zone_Top': data['person'].get('strikeZoneTop', 'TBD'),
						'Strike_Zone_Bottom': data['person'].get('strikeZoneBottom', 'TBD'),
					})
					if 'batSide' in data['person'].keys():
						data_dump.update({
							'Bat_Side_Code': data['person']['batSide'].get('code', 'TBD'),
							'Bat_Side_Description': data['person']['batSide'].get('description', 'TBD'),
						})
					if 'pitchHand' in data['person'].keys():
						data_dump.update({
							'Pitch_Hand_Code': data['person']['pitchHand'].get('code', 'TBD'),
							'Pitch_Hand_Description': data['person']['pitchHand'].get('description', 'TBD'),
						})
				if 'home' in data.keys():
					data_dump.update({
						'Home_City': data['home'].get('city', 'TBD'),
						'Home_State': data['home'].get('state', 'TBD'),
						'Home_Country': data['home'].get('country', 'TBD'),
					})
				if 'school' in data.keys():
					data_dump.update({
						'School_Name': data['school'].get('name', 'TBD'),
						'School_Class': data['school'].get('schoolClass', 'TBD'),
						'School_State': data['school'].get('state', 'TBD'),
						'School_Country': data['school'].get('country', 'TBD'),
					})
				if 'team' in data.keys():
					data_dump.update({
						'Team_ID': data['team'].get('id', 'TBD'),
						'Team_Name': data['team'].get('name', 'TBD'),
						'Team_Link': f"{ MLB_BASE_URL }{ data['team'].get('link', 'TBD') }",
						'ALL_Star_Status': data['team'].get('allStarStatus', 'TBD'),
					})
					if 'springLeague' in data['team'].keys():
						data_dump.update({
							'Spring_League_ID': data['team']['springLeague'].get('id', 'TBD'),
							'Spring_League_Name': data['team']['springLeague'].get('name', 'TBD'),
							'Spring_League_Link': f"{ MLB_BASE_URL } { data['team']['springLeague'].get('link', 'TBD') }",
						})
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Umpires() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/jobs/umpires').json()
		for data in response.get('roster'):
			data_dump: dict = {
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
				'Jersey_Number': data.get('jerseyNumber', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ MLB_BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_DataCasters() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(url = f'{MLB_BASE_URL}/api/v1/jobs/datacasters').json()
		for data in response.get('roster'):
			data_dump: dict = {
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ MLB_BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Players(team_name: str) -> dict:
	try:
		NBA_BASE_URL, dataset = 'https://balldontlie.io/api', []
		temp_response: dict = requests.get(url = f'{NBA_BASE_URL}/v1/players').json()
		total_pages: int = temp_response.get('meta', 'TBD').get('total_pages', 1)
		for i in range(1, int(total_pages) + 1):
			response: dict = requests.get(url = f'{NBA_BASE_URL}/v1/players?page={i}').json()
			for data in response.get('data'):
				if data['team']['full_name'] == team_name:
					dataset.append({
						'Player_ID': data.get('id', 'TBD'),
						'Player_Name': f"{ data.get('first_name', 'TBD') } {data.get('last_name', 'TBD') }",
						'Position': data['position'] if 'position' in data.keys() else 'TBD',
						'Team_Code': data['team'].get('abbreviation', 'TBD'), 'Team_City': data['team'].get('city', 'TBD'),
						'Team_Name': data['team'].get('name', 'TBD'), 'Team_Full_Name': data['team'].get('full_name', 'TBD'),
						'Team_Conference': data['team'].get('conference', 'TBD'), 'Team_Division': data['team'].get('division', 'TBD'),
					})
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Player_Profile(player_id: int) -> dict:
	try:
		payloads: dict = { 'PerMode': 'Totals', 'PlayerID': player_id }
		request_url: str = f'{NBA_BASE_URL}/stats/playerprofilev2?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_League_Players() -> dict:
	try:
		season_year: str = f"{ ( datetime.now() - timedelta(days = 365)).year }-{ str( datetime.now().year )[2:] }"
		payloads: dict = { 'IsOnlyCurrentSeason': 0, 'LeagueID': '00', 'Season': season_year }
		request_url: str = f'{NBA_BASE_URL}/stats/commonallplayers?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Live_Scoreboard(game_date: str) -> dict:
	try:
		payloads: dict = { 'DayOffset': 0, 'LeagueID': '00', 'GameDate': game_date }
		request_url: str = f'{NBA_BASE_URL}/stats/scoreboard?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_League_Standings() -> dict:
	try:
		season_year: str = f"{ ( datetime.now() - timedelta(days = 365)).year }-{ str( datetime.now().year )[2:] }" \
			if datetime.now().month < 10 else f"{ datetime.now().year }-{ str( (datetime.now() + timedelta(days = 365)).year )[2:] }"
		payloads: dict = { 'LeagueID': '00', 'Season': season_year, 'SeasonType' : 'Regular+Season' }
		request_url: str = f'{NBA_BASE_URL}/stats/leaguestandings?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Player_Awards(player_id: int) -> dict:
	try:
		request_url: str = f'{NBA_BASE_URL}/stats/playerawards?PlayerID={player_id}'
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Alltime_Leaders(limit: int) -> dict:
	try:
		payloads: str = { 'LeagueID': '00', 'PerMode': 'Totals', 'SeasonType': 'Regular+Season', 'TopX': int(limit)}
		request_url: str = f'{NBA_BASE_URL}/stats/alltimeleadersgrids?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(rul = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Team_Yearly_Stats(team_id: int) -> dict:
	try:
		payloads: dict = { 'LeagueID': '00', 'PerMode': 'Totals', 'SeasonType': 'Regular+Season', 'TeamID': int(team_id)}
		request_url: str = f'{NBA_BASE_URL}/stats/teamyearbyyearstats?' + \
			'&'.join( [ f'{key}={value}' for key, value in payloads.items() ] )
		response = requests.get(url = request_url, headers = NBA_STATIC_HEADERS, stream = True, timeout = 6000)
		return response.json()
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def NFL_Players_List() -> dict:
	try:
		dataset: list = []
		for letter in list(string.ascii_uppercase):
			dataset.append( pandas.read_html(f'{NFL_BASE_URL}/players/active/{letter}')[0] )
		return pandas.concat(objs = dataset, axis = 0)
	except Exception as ex:
		return {'error': ex}


@st.cache
def List_NBA_Live_Scoreboard_2(game_date: str) -> dict:
	try:
		dataset: list = []
		NBA_Teams: dict = { str(data.get('ID')) : data.get('Team_Name') for data in NBA_TEAMS }
		response: dict = requests.get(f'{NBA_BASE_URL_2}/v2/{game_date}/scoreboard.json').json()
		for data in response.get('games'):
			data_dump: dict = {
				'Game ID': data.get('gameId', 'TBD'),
				'Game_Date': datetime.strptime(game_date, '%Y%m%d').strftime('%d-%b-%Y') \
					if 'startDateEastern' in data.keys() else 'TBD',
				'Game_Time': data.get('startTimeEastern', 'TBD'),
				'Game_URL_Code': data.get('gameUrlCode', 'TBD'),
				'Game_Duration': data.get('gameDuration', 'TBD'),
				'Attendance': data.get('attendance', 'TBD'),
			}
			if 'vTeam' in data.keys():
				data_dump.update({
					'Visitor_Team_ID': data['vTeam'].get('teamId', 'TBD'),
					'Visitor_Team_Name': NBA_Teams.get(data['vTeam'].get('teamId', 'TBD'), 'TBD'),
					'Visitor_Team_Code': data['vTeam'].get('triCode', 'TBD'),
					'Visitor_Team_Score': data['vTeam'].get('score', 'TBD'),
					'Visitor_Team_LineScore': data['vTeam'].get('linescore', 'TBD')
				})
			if 'hTeam' in data.keys():
				data_dump.update({
					'Home_Team_ID': data['hTeam'].get('teamId', 'TBD'),
					'Home_Team_Name': NBA_Teams.get(data['hTeam'].get('teamId', 'TBD'), 'TBD'),
					'Home_Team_Code': data['hTeam'].get('triCode', 'TBD'),
					'Home_Team_Score': data['hTeam'].get('score', 'TBD'),
					'Home_Team_LineScore': data['hTeam'].get('linescore', 'TBD')
				})
			if 'tickets' in data.keys():
				data_dump.update({
					'Mobile_App': data['tickets'].get('mobileApp', 'TBD'),
					'Desktop_Web': data['tickets'].get('desktopWeb', 'TBD'),
					'Mobile_Web': data['tickets'].get('mobileWeb', 'TBD'),
					'League_Game_Info': data['tickets'].get('leagGameInfo', 'TBD'),
				})
			if 'arena' in data.keys():
				data_dump.update({
					'Arena_Name': data['arena'].get('name', 'TBD'),
					'Is_Domestic': 'Yes' if data['arena'].get('isDomestic') == True else 'False'\
						if data['arena'].get('isDomestic') == False else 'TBD',
					'City': data['arena'].get('city', 'TBD'), 'Country': data['arena'].get('country', 'TBD'),
				})
			if 'broadcasters' in data['watch']['broadcast'].keys():
				broadcasters = data['watch']['broadcast']['broadcasters']
				data_dump.update({
					'VTeam_Broadcaster': [data.get('longName', 'TBD') for data in broadcasters.get('vTeam')],
					'HTeam_Broadcaster': [data.get('longName', 'TBD') for data in broadcasters.get('hTeam')],
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_NBA_Coaches() -> dict:
	try:
		dataset, year = [], datetime.now().year
		NBA_Teams: dict = { str(data.get('ID')) : data.get('Team_Name') for data in NBA_TEAMS }
		response: dict = requests.get(f'{NBA_BASE_URL_2}/v1/{year}/coaches.json').json()
		for data in response.get('league').get('standard'):
			data_dump: dict = {
				'Team_ID': data.get('teamId', 'TBD'), 'Person_ID': data.get('personId', 'TBD'),
				'Team_Name': NBA_Teams.get( data.get('teamId', 'TBD'), 'TBD'), 'College': data.get('college', 'TBD'),
				'First_Name': data.get('firstName', 'TBD'), 'Last_Name': data.get('lastName', 'TBD'),
				'Is_Assistant': 'Yes' if data.get('isAssistant') == True else 'No',
			}
			if 'teamSitesOnly' in data.keys():
				data_dump.update({
					'Display_Name': data['teamSitesOnly'].get('displayName', 'TBD'), 
					'Coach_Code': data['teamSitesOnly'].get('coachCode', 'TBD'),
					'Coach_Role': data['teamSitesOnly'].get('coachRole', 'TBD'), 
					'Team_Code': data['teamSitesOnly'].get('teamTricode', 'TBD'),
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }

#---------------------------------------------------------------------------------------------------------------------------------#

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

	col_1, col_2, col_3 = st.beta_columns((2, 2, 2))
	CATEGORY: str = col_1.selectbox(label = 'Choose Category', options = list(CATEGORIES.keys()) )
	st.write('*' * 50)

	if CATEGORY == 'Catalog':
		st.write('** Catalog ** Page Shows the List of Micro Apps Based on Category & Sub-Category in this Web Application.')
		st.table( data = [{'CATEGORY': key, 'SUB_CATEGORY': data} for key, value in CATEGORIES.items() \
			if value is not None for data in value] )

	elif CATEGORY == 'Cricket Stats':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'Cricket Stats':
			try:
				st.subheader('** Cricket Stats **')
				dataset = Cricket_Stats()
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				with st.beta_expander(label = 'List of Cricket Stats Categories?', expanded = False):
					st.dataframe( data = dataset )
				category: str = col_2.selectbox(label = 'Choose Category', options = list(dataset.category.unique()) )
				dataset = dataset[ dataset.category == category ]
				sub_category: str = col_3.selectbox(label = 'Choose Sub Category', options = list(dataset.sub_category.unique()) )
				dataset = dataset[ dataset.sub_category == sub_category ]
				dataset = pandas.read_html( CRICKET_STATS_BASE_URL.format(f'{ list( dataset.sub_category_id )[0] }.html') )[0]
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'MLB League':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'About MLB':
			st.subheader('** About MLB **')
			st.write(''' The Major League Baseball (MLB) is an American Professional Baseball Organization and The Oldest of the 
				Major Professional Sports Leagues in the United States and Canada. A Total of 30 Teams Play in Major League Baseball: 
				15 Teams in the National League (NL) and 15 in the American League (AL). The NL and AL were Formed as Separate Legal 
				Entities in 1876 and 1901 Respectively. Beginning in 1903, the Two Leagues Cooperated But Remained Legally Separate 
				Entities. Both leagues Operated as Legally Separate Entities Until They Merged into a Single Organization Led by the 
				Commissioner of Baseball in 2000. MLB also Oversees Minor League Baseball, Which Comprises 256 Teams Affiliated With 
				the Major League Clubs. MLB and the World Baseball Softball Confederation Jointly Manage the International World 
				Baseball Classic tournament. ''')
			st.markdown( body = f"<img src = 'https://www.mlbstatic.com/team-logos/league-on-dark/1.svg' width = 700 \
				height = 400>", unsafe_allow_html = True )

		elif SUB_CATEGORY == 'MLB Teams':
			try:
				st.subheader('** MLB Teams **')
				dataset = pandas.DataFrame( data = List_MLB_Teams()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Sports':
			try:
				st.subheader('** MLB Sports **')
				dataset = pandas.DataFrame( data = List_MLB_Sports()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Players':
			try:
				st.subheader('** MLB Players **')
				Sports: dict = { Sport['Sport_Name']: int(Sport['Sport_ID']) for Sport in List_MLB_Sports()['data'] }
				Sport: str = col_3.selectbox(label = 'Select MLB Sport', options = list(Sports.keys()) )
				st.write(f'** > Selected ** Sport Name = { Sport } | Sport ID = { Sports[Sport] } ')
				dataset = pandas.DataFrame( data = List_MLB_Players( sport_id = Sports[Sport] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Leagues':
			try:
				st.subheader('** MLB Leagues **')
				dataset = pandas.DataFrame( data = List_MLB_Leagues()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Divisions':
			try:
				st.subheader('** MLB Divisions **')
				dataset = pandas.DataFrame( data = List_MLB_Divisions()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Schedule':
			try:
				st.subheader('** MLB Schedule **')
				Sports: dict = { Sport['Sport_Name']: int(Sport['Sport_ID']) for Sport in List_MLB_Sports()['data'] }
				Sport: str = col_3.selectbox(label = 'Select MLB Sport', options = list(Sports.keys()) )
				Start_Date = col_1.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 5)) )
				End_Date = col_2.date_input(label = 'End Date', value = (datetime.now() + timedelta(days = 30)) )
				st.write(f'** > Selected ** MLB Sport Name =  { Sport } | Sport ID = { Sports[Sport] } ')
				st.write(f'** > Selected ** Start Date = { Start_Date } | End Date = { End_Date } ')
				dataset = pandas.DataFrame( data = List_MLB_Schedule( sport_id = Sports[Sport], 
					start_date = Start_Date, end_date = End_Date )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Team Rosters':
			try:
				st.subheader('** MLB Team Rosters **')
				Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
				Team: str = col_3.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
				st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
				dataset = pandas.DataFrame( data = List_MLB_Rosters( team_id = Teams[Team] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Team Personnel':
			try:
				st.subheader('** MLB Team Personnel **')
				Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
				Team: str = col_3.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
				st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
				dataset = pandas.DataFrame( data = List_MLB_Personnel( team_id = Teams[Team] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Team Coaches':
			try:
				st.subheader('** MLB Team Coaches **')
				Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
				Team: str = col_3.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
				st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
				dataset = pandas.DataFrame( data = List_MLB_Coaches( team_id = Teams[Team] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Attendances':
			try:
				st.subheader('** MLB Attendances **')
				Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
				Team: str = col_3.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
				st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
				dataset = pandas.DataFrame( data = List_MLB_Attendances( team_id = Teams[Team] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Venues':
			try:
				st.subheader('** MLB Venues **')
				dataset = pandas.DataFrame( data = List_MLB_Venues()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Alumnis':
			try:
				st.subheader('** MLB Alumnis **')
				Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
				Team: str = col_3.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
				st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
				dataset = pandas.DataFrame( data = List_MLB_Alumnis( team_id = Teams[Team] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB League Standings':
			try:
				st.subheader('** MLB League Standings **')
				Leagues: dict = { League['League_Name']: int(League['League_ID']) for League in List_MLB_Leagues()['data'] }
				League: str = col_3.selectbox(label = 'Select MLB League', options = list(Leagues.keys()) )
				st.write(f'** > Selected ** MLB League Name =  { League } | League ID = { Leagues[League] } ')
				dataset = pandas.DataFrame( data = List_MLB_League_Standings( league_id = Leagues[League] )['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Drafts':
			try:
				st.subheader('** MLB Drafts **')
				dataset = pandas.DataFrame( data = List_MLB_Drafts()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB Umpires':
			try:
				st.subheader('** MLB Umpires **')
				dataset = pandas.DataFrame( data = List_MLB_Umpires()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'MLB DataCasters':
			try:
				st.subheader('** MLB DataCasters **')
				dataset = pandas.DataFrame( data = List_MLB_Umpires()['data'] )
				dataset.fillna('TBD', inplace = True)
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'NBA League':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'About NBA':
			st.subheader('** About NBA **')
			st.write('''The National Basketball Association (NBA) is an American Men's Professional Basketball League. It is 
				Composed of 30 Teams and is One of the 4 Major Professional Sports Leagues in the United States and Canada. 
				It is Widely Considered to be the Premier Men's Professional Basketball League in the World.''')
			st.markdown( body = f"<img src = 'https://wallpapercave.com/wp/wp1827442.jpg' width = 700 height = 400>", 
				unsafe_allow_html = True )

		elif SUB_CATEGORY == 'NBA Teams':
			try:
				st.subheader('** NBA Teams **')
				dataset = pandas.DataFrame( data = NBA_TEAMS )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
				st.write('** NBA Teams by Division Split **')
				pivot_division = pandas.pivot_table(dataset, index = 'Division', 
					values = 'Team_Name', aggfunc = 'count', fill_value = 0)
				st.dataframe( data = pivot_division )
				st.write('** NBA Teams by Conference Split **')
				pivot_conference = pandas.pivot_table(dataset, index = 'Conference', 
					values = 'Team_Name', aggfunc = 'count', fill_value = 0)
				st.dataframe( data = pivot_conference )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA ScoreBoard 2':
			try:
				st.subheader('** NBA Live ScoreBoard 2 **')
				response: dict = requests.get(f'{NBA_BASE_URL_2}/v2/calendar.json').json()
				Match_Dates: list = [{'Date' : date, 'Games' : games} for date, games in response.items() \
					if date.isnumeric() and date >= (datetime.now() - timedelta(days=2)).strftime('%Y%m%d') and games > 1]
				Dates: list = [ data.get('Date') for data in Match_Dates ]
				game_date: str = col_3.selectbox(label = 'Select Match Date (YYYYMMDD)', options = Dates)
				dataset = pandas.DataFrame( data = List_NBA_Live_Scoreboard_2( game_date = game_date )['data'] )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA Players':
			try:
				st.subheader('** NBA League Players **')
				NBA_Teams: list = [ data['Team_Name'] for data in NBA_TEAMS]
				team_name: str = col_3.selectbox(label = 'Select NBA Team', options = NBA_Teams)
				dataset = pandas.DataFrame( data = List_NBA_Players( team_name = team_name )['data'] )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA Player Profile':
			try:
				st.subheader('** NBA Player Profile **')
				st.write('Get Player ID by Search Name from Official NBA Stats -> https://stats.nba.com/players/')
				League_Players: dict = List_NBA_League_Players()['resultSets'][0]
				player_names: list = [ data[2] for data in League_Players['rowSet'] ]
				player_name: str = col_1.selectbox(label = 'Choose NBA Player', options = player_names )
				player_id: int = [ data[0] for data in League_Players['rowSet'] if data[2] == player_name ][0]
				st.write(f'** NBA Player ID : ** { player_id } ** | Player Name : ** { player_name } ')
				Player_Profile: dict = List_NBA_Player_Profile( player_id  = player_id )
				st.write('** NBA Player Awards **')
				Player_Awards: dict = List_NBA_Player_Awards( player_id  = player_id )['resultSets'][0]
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
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA League Players':
			try:
				st.subheader('** NBA All League Players **')
				League_Players: dict = List_NBA_League_Players()['resultSets'][0]
				dataset = pandas.DataFrame( data = League_Players['rowSet'], columns = League_Players['headers'] )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA Coaches':
			try:
				st.subheader('** NBA League Coaches **')
				dataset = pandas.DataFrame( data = List_NBA_Coaches()['data'] )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA ScoreBoard 1':
			try:
				st.subheader('** NBA Live ScoreBoard 1 **')
				game_date: str = col_1.date_input(label = 'Choose Game Date', value = datetime.now() )
				dataset: dict = List_NBA_Live_Scoreboard( game_date = game_date )
				titles: list = [ data['name'] for data in dataset['resultSets'] ]
				sub_category: str = col_2.selectbox(label = 'Select Sub Category', options = titles )
				for data in dataset['resultSets']:
					if sub_category == data['name']:
						st.write(f"** Selected Date | Sub Category : ** { game_date.strftime('%d-%b-%Y')  } | { sub_category } ")
						data_frame = pandas.DataFrame( data = data['rowSet'], columns = data['headers'] )
						st.markdown( body = Excel_Downloader( df = data_frame ), unsafe_allow_html = True)
						st.dataframe( data = data_frame )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA League Standings':
			try:
				st.subheader('** NBA League Standings **')
				data_dump: dict = List_NBA_League_Standings()['resultSets'][0]
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
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA All Time Leaders':
			try:
				st.subheader('** NBA All Time Leaders **')
				headings: dict = {'GPLeaders': 'Games Player', 'PTSLeaders': 'Points', 'ASTLeaders': 'Assists', 'STLLeaders': 'Steals', 
					'OREBLeaders': 'Offensive Rebounds', 'REBLeaders': 'Rebounds', 'BLKLeaders': 'Blocks', 'TOVLeaders': 'Turnovers',
					'FGMLeaders': 'Field Goals Made', 'FGALeaders': 'Field Goals Attempted', 'FG_PCTLeaders': 'Field Goals %', 
					'FG3MLeaders': 'Three Pointers Made', 'FG3ALeaders': 'Three Pointers Attempted', 'PFLeaders': 'Personal Fouls', 
					'FG3_PCTLeaders': 'Three Point %', 'FTMLeaders': 'Free Throws Made', 'FTALeaders': 'Free Throws Attempted', 
					'FT_PCTLeaders': 'Free Throws %', 'DREBLeaders': 'Defensive Rebounds' }
				limit: int = col_3.slider(label = 'How Many Players ?', min_value = 0, max_value = 1000, value = 5, step = 5)
				for _, dataset in enumerate( iterable = List_NBA_Alltime_Leaders( limit = limit )['resultSets'] ):
					st.write(f"** { headings[ dataset['name'] ] } Leaders **")
					data_frame = pandas.DataFrame( data = dataset['rowSet'], columns = dataset['headers'] )
					st.markdown( body = Excel_Downloader( df = data_frame ), unsafe_allow_html = True)
					st.dataframe( data = data_frame )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NBA Team Yearly Stats':
			try:
				st.subheader('** NBA Team Yearly Stats **')
				League_Standings: dict = List_NBA_League_Standings()['resultSets'][0]
				NBA_Teams = pandas.DataFrame( data = League_Standings['rowSet'], columns = League_Standings['headers'] )
				NBA_Teams['Team_Name'] = NBA_Teams['TeamCity'] + ' ' + NBA_Teams['TeamName']
				NBA_Teams: dict = { tid : tname for tid, tname in zip( list(NBA_Teams.TeamID.unique()), list(NBA_Teams.Team_Name.unique()) ) }
				team_name: str = col_3.selectbox(label = 'Select NBA Team', options = list(NBA_Teams.values()) )
				for TEAM_ID, TEAM_NAME in NBA_Teams.items():
					if TEAM_NAME == team_name:
						data_dump: dict = List_NBA_Team_Yearly_Stats( team_id = TEAM_ID )['resultSets'][0]
						dataset = pandas.DataFrame( data = data_dump['rowSet'], columns = data_dump['headers'] )
						st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
						st.dataframe( data = dataset )
						st.write(f'** { TEAM_NAME } - Championship Titles Count **')
						pivot_titles = pandas.pivot_table(dataset, index = 'NBA_FINALS_APPEARANCE', 
							values = 'TEAM_NAME', aggfunc = 'count', fill_value = 0)
						st.dataframe( data = pivot_titles )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'NFL League':
		SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

		if SUB_CATEGORY == 'About NFL':
			st.subheader('** About NFL **')
			st.write(""" The National Football League (NFL) is a Professional American Football League Consisting 
				of 32 Teams, Divided Equally Between the National Football Conference (NFC) and the American Football 
				Conference (AFC). The NFL is One of the Four Major North American Professional Sports Leagues, The 
				Highest Professional Level of American football in the World, The Wealthiest Professional Sport 
				League by Revenue, and The Sport League With The Most Valuable Teams. The NFL's 17-week Regular 
				Season Runs From Early September to Late December, With Each Team Playing 16 Games and Having 1 Bye 
				week. Following the Conclusion of the Regular Season, 7 Teams From Each Conference (4 Division 
				Winners and 3 Wild Card Teams) Advance to The Playoffs, A Single-Elimination Tournament Culminating 
				in The Super Bowl, Which is Usually Held on The First Sunday in February and is Played Between The 
				Champions of the NFC and AFC.""")
			st.markdown( body = f"<img src = 'https://koamnewsnow.com/content/uploads/2020/04/NFL-logo.jpg' width = 700 \
				height = 400>", unsafe_allow_html = True )

		elif SUB_CATEGORY == 'NFL Teams':
			try:
				st.subheader('** NFL Teams **')
				dataset = pandas.DataFrame( data = NFL_TEAMS )
				st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
				st.write(f'**> Total NFL Teams = ** { len( dataset ) } ')
				st.dataframe( data = dataset )
				col_1.write('** NBA Teams by Division Split **')
				pivot_division = pandas.pivot_table(dataset, index = 'Division', 
					values = 'Team_Name', aggfunc = 'count', fill_value = 0)
				col_1.dataframe( data = pivot_division )
				col_2.write('** NBA Teams by Conference Split **')
				pivot_conference = pandas.pivot_table(dataset, index = 'Conference', 
					values = 'Team_Name', aggfunc = 'count', fill_value = 0)
				col_2.dataframe( data = pivot_conference )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NFL Players':
			try:
				st.subheader('** NFL Players **')
				dataset = NFL_Players_List()
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				team_name: str = col_3.selectbox(label = 'Select NFL Team', options = list( set( dataset['Current Team'].unique() ) ) )
				st.dataframe( data = dataset[ dataset['Current Team'] == team_name ] )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NFL Standings':
			try:
				st.subheader('** NFL Standings **')
				category: str = col_3.selectbox(label = 'Select Category', options = ('Division', 'Conference', 'League') )
				year: int = st.slider(label = 'Select Year', min_value = 1950, max_value = datetime.now().year,
					value = (datetime.now() - timedelta(days = 365)).year, step = 1 )
				data_dump = pandas.read_html(f'{NFL_BASE_URL}/standings/{category}/{year}/REG')
				for dataset in data_dump:
					st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
					st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NFL Team Stats':
			try:
				st.subheader('** NFL Team Stats **')
				filter_1: str = col_1.selectbox(label = 'Select Filter 1', options = ('Offense', 'Defence', 'Special-Teams') )
				filter_2: str = col_2.selectbox(label = 'Select Filter 2', options = ('Passing', 'Rushing', 'Receiving', 'Scoring', 'Downs',
					'Field-Goals', 'Kickoffs', 'Kickoff-Returns', 'Punt-Returns') )
				year: int = col_3.slider(label = 'Select Year', min_value = 1950, max_value = datetime.now().year,
					value = (datetime.now() - timedelta(days = 365)).year, step = 1 )
				try:
					dataset = pandas.read_html(f'{NFL_BASE_URL}/stats/team-stats/{filter_1}/{filter_2}/{year}/REG/all')[0]
				except:
					dataset = pandas.DataFrame( data = [] )
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')

		elif SUB_CATEGORY == 'NFL Player Stats':
			try:
				st.subheader('** NFL Player Stats **')
				categories: dict = {'Passing': 'PassingYards', 'Rushing': 'RushingYards', 'Receiving': 'ReceivingReceptions',
					'Fumble': 'DefensiveForcedFumble', 'Tackles': 'DefensiveCombineTackles', 'Interceptions': 'DefensiveInterceptions',
					'Field-Goals': 'KickingFGMade', 'Kickoffs': 'KickoffTotal', 'Kickoff-Returns': 'KickReturnAverageYards',
					'Punts': 'PuntingAverageYards', 'Punt-Returns': 'PuntReturnsAverageYards'} 
				filter_1: str = col_3.selectbox(label = 'Select Stats Category', options = list(categories.keys()) )
				filter_2: int = st.slider(label = 'Select Year', min_value = 1950, max_value = datetime.now().year,
					value = (datetime.now() - timedelta(days = 365)).year, step = 1 )
				dataset = pandas.read_html(f'{NFL_BASE_URL}/stats/player-stats/category/{filter_1}/{filter_2}/REG/all/{categories[filter_1]}/desc')[0]
				st.markdown( body = Excel_Downloader( dataset ), unsafe_allow_html = True)
				st.dataframe( data = dataset )
			except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'Cricket IPL Stats':
		try:
			SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )
			options: list = ['all-time'] + [data for data in range(2008, datetime.now().year + 1)]
			IPL_Category: str = col_3.selectbox(label = 'Select IPL Year / All-Time ?', options = options)
			BASE_URL: str = f'{IPL_BASE_URL}/{IPL_Category}'
				
			if SUB_CATEGORY == 'About IPL':
				try:
					st.subheader('** About IPL **')
					st.write(''' The Indian Premier League (IPL) is a Professional Twenty20 Cricket League in India Contested 
						During March or April and May of Every Year by 8 Teams Representing 8 Different Cities (or) States in India.
						The League was Founded by The Board of Control for Cricket in India (BCCI) in 2008. The IPL has an Exclusive 
						Window in ICC Future Tours Programme. ''')
					st.subheader('** IPL Teams **')
					dataset = pandas.DataFrame( data = IPL_TEAMS )
					st.markdown( body = f"<img src = 'https://miro.medium.com/max/626/0*BAwYmCO5tos8RCO1.png' width = 700 \
						height = 400>", unsafe_allow_html = True )
				except Exception as ex:
					st.error(f'** Error : ** { ex } ')

			elif SUB_CATEGORY == 'IPL Winners':
				try:
					st.subheader('** IPL Winners **')
					dataset = pandas.read_html( requests.get('https://sportskeeda.com/cricket/ipl-winners-list', 
						headers = { 'User-Agent': UserAgent().random }).text )[0]
					new_header = dataset.iloc[0] 
					dataset = dataset[1 : ] 
					dataset.columns = new_header
				except Exception as ex:
					st.error(f'** Error : ** { ex } ')

			elif SUB_CATEGORY == 'Most Runs':	
				st.subheader('** Most Runs **')
				dataset = pandas.read_html(f'{BASE_URL}/most-runs')[0]

			elif SUB_CATEGORY == 'Most Sixes':
				st.subheader('** Most Sixes **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-sixes')[0]

			elif SUB_CATEGORY == 'Most Sixes in Innings':
				st.subheader('** Most Sixes in Innings **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-sixes-innings')[0]

			elif SUB_CATEGORY == 'Highest Scores':
				st.subheader('** Highest Scores **')	
				dataset = pandas.read_html(f'{BASE_URL}/highest-scores')[0]

			elif SUB_CATEGORY == 'Best Strike Rate':
				st.subheader('** Best Strike Rate **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate')[0]

			elif SUB_CATEGORY == 'Best Strike Rate in Innings':
				st.subheader('** Best Strike Rate in Innings **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-batting-strike-rate-innings')[0]

			elif SUB_CATEGORY == 'Best Batting Average':
				st.subheader('** Best Batting Average **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-batting-average')[0]

			elif SUB_CATEGORY == 'Most Fifties':
				st.subheader('** Most Fifties **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-fifties')[0]

			elif SUB_CATEGORY == 'Most Centuries':
				st.subheader('** Most Centuries **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-centuries')[0]

			elif SUB_CATEGORY == 'Most Fours':
				st.subheader('** Most Fours **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-fours')[0]

			elif SUB_CATEGORY == 'Fastest Fifties':
				st.subheader('** Fastest Fifties **')	
				dataset = pandas.read_html(f'{BASE_URL}/fastest-fifties')[0]

			elif SUB_CATEGORY == 'Fastest Centuries':
				st.subheader('** Fastest Centuries **')	
				dataset = pandas.read_html(f'{BASE_URL}/fastest-centuries')[0]

			elif SUB_CATEGORY == 'Most Wickets':
				st.subheader('** Most Wickets **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-wickets')[0]

			elif SUB_CATEGORY == 'Best Bowling in Innings':
				st.subheader('** Best Bowling in Innings **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-innings')[0]

			elif SUB_CATEGORY == 'Best Bowling Average':
				st.subheader('** Best Bowling Average **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-average')[0]

			elif SUB_CATEGORY == 'Best Bowling Economy':
				st.subheader('** Best Bowling Economy **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-economy')[0]

			elif SUB_CATEGORY == 'Best Bowling Average Strike Rate in Innings':
				st.subheader('** Best Bowling Average Strike Rate in Innings **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate-innings')[0]

			elif SUB_CATEGORY == 'Best Bowling Average Strike Rate':
				st.subheader('** Best Bowling Average Strike Rate **')	
				dataset = pandas.read_html(f'{BASE_URL}/best-bowling-strike-rate')[0]

			elif SUB_CATEGORY == 'Most Runs Conceded':
				st.subheader('** Most Runs Conceded **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-runs-conceded-innings')[0]

			elif SUB_CATEGORY == 'Most Dot Balls':
				st.subheader('** Most Dot Balls **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-dot-balls')[0]

			elif SUB_CATEGORY == 'Most Maiden Overs':
				st.subheader('** Most Maiden Overs **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-maidens')[0]

			elif SUB_CATEGORY == 'Most 4 Wickets':
				st.subheader('** Most 4 Wickets **')	
				dataset = pandas.read_html(f'{BASE_URL}/most-four-wickets')[0]

			elif SUB_CATEGORY == 'Points Table':
				st.subheader('** Points Table **')
				if IPL_Category == 'all-time':	st.write('** No Point Table for All Time Stats in IPL! **')
				dataset = pandas.read_html(f'https://iplt20.com/points-table/{IPL_Category}')[0]
				dataset.rename(columns = {'Unnamed: 0': 'Rank', 'Pld': 'Matches', 'Pts': 'Points'}, inplace = True)
				dataset = dataset[['Rank', 'Team', 'Matches', 'Won', 'Lost', 'Tied', 'N/R', 'Net RR', 'Points']]
			
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'Cricket ICC Rankings':
		try:
			SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

			if SUB_CATEGORY == 'Test Team Stats':
				st.write('** Test Team Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/team-rankings/test')[0]

			elif SUB_CATEGORY == 'Test Player Batting Stats':
				st.write('** Test Player Batting Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/test/batting')[0]

			elif SUB_CATEGORY == 'Test Player Bowling Stats':
				st.write('** Test Player Bowling Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/test/bowling')[0]

			elif SUB_CATEGORY == 'Test Player All-Rounder Stats':
				st.write('** Test Player All-Rounder Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/test/all-rounder')[0]

			elif SUB_CATEGORY == 'ODI Team Stats':
				st.write('** ODI Team Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/team-rankings/odi')[0]

			elif SUB_CATEGORY == 'ODI Player Batting Stats':
				st.write('** ODI Player Batting Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/odi/batting')[0]

			elif SUB_CATEGORY == 'ODI Player Bowling Stats':
				st.write('** ODI Player Bowling Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/odi/bowling')[0]

			elif SUB_CATEGORY == 'ODI Player All-Rounder Stats':
				st.write('** ODI Player All-Rounder Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/odi/all-rounder')[0]

			elif SUB_CATEGORY == 'T20I Team Stats':
				st.write('** T20I Team Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/team-rankings/t20i')[0]

			elif SUB_CATEGORY == 'T20I Player Batting Stats':
				st.write('** T20I Player Batting Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/t20i/batting')[0]

			elif SUB_CATEGORY == 'T20I Player Bowling Stats':
				st.write('** T20I Player Bowling Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/t20i/bowling')[0]

			elif SUB_CATEGORY == 'T20I Player All-Rounder Stats':
				st.write('** T20I Player All-Rounder Stats **')
				dataset = pandas.read_html(f'{ICC_BASE_URL}/player-rankings/t20i/all-rounder')[0]
			
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
				st.error(f'** Error : ** { ex } ')


	elif CATEGORY == 'Cricket WC Stats':
		try:
			SUB_CATEGORY: str = col_2.selectbox(label = 'Choose Sub Category', options = CATEGORIES[CATEGORY] )

			if SUB_CATEGORY == 'About Cricket World Cup':
				st.write('** About Cricket World Cup **')
				st.write(''' The Cricket World Cup (officially known as ICC Men's Cricket World Cup) is the International 
					Championship of One Day International (ODI) Cricket. The Event is Organised By The Sport's Governing Body, 
					The International Cricket Council (ICC), Every 4 Years, with Preliminary Qualification Rounds Leading Up 
					to a Finals Tournament. The tournament is One of The World's Most Viewed Sporting Events and is Considered 
					the Flagship Event of The Tnternational Cricket Calendar' by the ICC. ''')
				st.markdown( body = f"<img src = 'https://tinyurl.com/y5mwtglb' width = 700 height = 400>", unsafe_allow_html = True )
				dataset = pandas.DataFrame( data = [] )

			elif SUB_CATEGORY == 'ICC Cricket World Cup Winners':
				st.write('** ICC Cricket World Cup Winners **')
				dataset = pandas.read_html( requests.get('https://sportskeeda.com/cricket/cricket-world-cup-winners', 
					headers = { 'User-Agent': UserAgent().random } ).text )[0]
				new_header = dataset.iloc[0] 
				dataset = dataset[1 : ] 
				dataset.columns = new_header

			elif SUB_CATEGORY == 'Most Runs':
				st.write('** Most Runs **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-runs')[0]

			elif SUB_CATEGORY == 'Highest Scores':
				st.write('** Highest Scores **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/highest-score')[0]

			elif SUB_CATEGORY == 'Best Batting Average':
				st.write('** Best Batting Average **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-batting-average')[0]

			elif SUB_CATEGORY == 'Best Batting Strike Rate':
				st.write('** Best Batting Strike Rate **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-batting-strike-rate')[0]

			elif SUB_CATEGORY == 'Best Batting Strike Rate Innings':
				st.write('** Best Batting Strike Rate Innings **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-batting-strike-rate-innings')[0]

			elif SUB_CATEGORY == 'Most Centuries':
				st.write('** Most Centuries **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-centuries')[0]

			elif SUB_CATEGORY == 'Fastest Centuries':
				st.write('** Fastest Centuries **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/fastest-centuries')[0]

			elif SUB_CATEGORY == 'Most Fifties':
				st.write('** Most Fifties **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-fifties')[0]

			elif SUB_CATEGORY == 'Fastest Fifties':
				st.write('** Fastest Fifties **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/fastest-fifties')[0]

			elif SUB_CATEGORY == 'Most Sixes':
				st.write('** Most Sixes **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-sixes')[0]

			elif SUB_CATEGORY == 'Most Fours':
				st.write('** Most Fours **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-fours')[0]

			elif SUB_CATEGORY == 'Most Wickets':
				st.write('** Most Wickets **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-wickets')[0]

			elif SUB_CATEGORY == 'Best Bowling Average':
				st.write('** Best Bowling Average **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-average')[0]

			elif SUB_CATEGORY == 'Best Bowling Economy':
				st.write('** Best Bowling Economy **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-economy')[0]

			elif SUB_CATEGORY == 'Best Bowling Economy Innings':
				st.write('** Best Bowling Economy Innings **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-economy-innings')[0]

			elif SUB_CATEGORY == 'Best Bowling Strike Rate':
				st.write('** Best Bowling Strike Rate **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-strike-rate')[0]

			elif SUB_CATEGORY == 'Best Bowling Strike Rate Innings':
				st.write('** Best Bowling Strike Rate Innings **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-strike-rate-innings')[0]

			elif SUB_CATEGORY == 'Best Bowling Figures':
				st.write('** Best Bowling Figures **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-bowling-figures')[0]

			elif SUB_CATEGORY == 'Most Maidens':
				st.write('** Most Maidens **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-maidens')[0]

			elif SUB_CATEGORY == 'Most Dot Balls':
				st.write('** Most Dot Balls **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-dot-balls')[0]

			elif SUB_CATEGORY == 'Most Dot Balls Innings':
				st.write('** Most Dot Balls Innings **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-dot-balls-innings')[0]

			elif SUB_CATEGORY == 'Best Win Percetage':
				st.write('** Best Win Percetage **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/best-win-percentage')[0]

			elif SUB_CATEGORY == 'Most Wins':
				st.write('** Most Wins **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-wins')[0]

			elif SUB_CATEGORY == 'Most Losses':
				st.write('** Most Losses **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/most-losses')[0]

			elif SUB_CATEGORY == 'Highest Match Aggregate':
				st.write('** Highest Match Aggregate **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/highest-match-aggregates')[0]

			elif SUB_CATEGORY == 'Largest Victories Runs':
				st.write('** Largest Victories Runs **')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/largest-victories-runs')[0]

			elif SUB_CATEGORY == 'Largest Victories Wickets':
				st.write('**  Largest Victories Wickets**')
				dataset = pandas.read_html(f'{ICC_CWC_BASE_URL}/largest-victories-wickets')[0]
			
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
				st.error(f'** Error : ** { ex } ')


#---------------------------------------------------------------------------------------------------------------------------------#

## Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#---------------------------------------------------------------------------------------------------------------------------------#