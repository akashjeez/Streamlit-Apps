__author__ = 'akashjeez'

import os, io, base64, pandas, requests
from datetime import datetime, timedelta
import streamlit as st
from dateutil import parser

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('NFL😎L€@gU€')

#----------------------------------------------------------------------------------------------------------------------#

## Refernce => http://static.nfl.com/liveupdate/scores/scores.json
# https://static.nfl.com/liveupdate/game-center/2020101600/2020101600_gtd.json
# https://static.nfl.com/ajax/scorestrip?season=2020&seasonType=REG&week=1

BASE_URL = 'https:/nfl.com'

CATEGORIES_LIST: list = ['About NFL', 'NFL Teams', ]
CATEGORIES_LIST.sort()

## NFL Teams List.
NFL_TEAMS = [
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
def List_MLB_Sports() -> dict:
	try:
		response: dict = requests.get(f'{BASE_URL}/api/v1/sports').json()
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

	if CATEGORY == 'About NFL':
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
		st.markdown( f"<img src = 'https://koamnewsnow.com/content/uploads/2020/04/NFL-logo.jpg' width = 700 \
			height = 400>", unsafe_allow_html = True )

	elif CATEGORY == 'NFL Teams':
		try:
			st.subheader('** NFL Teams **')
			col_1, col_2 = st.beta_columns((2, 2))
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
			st.write(f'\n ** Error : { ex } **')


#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#