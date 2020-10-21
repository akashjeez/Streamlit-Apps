__author__ = 'akashjeez'

import os, io, base64, pandas, requests
from datetime import datetime, timedelta
import streamlit as st
from dateutil import parser

#----------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('ML₿😎L€@gU€')

#----------------------------------------------------------------------------------------------------------------------#

## Refernce => https://pypi.org/project/MLB-StatsAPI/

BASE_URL = 'https://statsapi.mlb.com'

CATEGORIES_LIST: list = ['About MLB', 'MLB Teams', 'MLB Sports', 'MLB Players', 'MLB Leagues', 'MLB Schedule',
	'MLB Team Rosters', 'MLB Team Personnel', 'MLB Team Coaches', 'MLB Attendances', 'MLB Venues', 'MLB Alumnis',
	'MLB League Standings', 'MLB Divisions', 'MLB Drafts', 'MLB Umpires', 'MLB DataCasters']
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
def List_MLB_Teams() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/teams').json()
		for data in response['teams']:
			data_dump = {
				'Team_ID': data.get('id', 'TBD'),
				'Team_Name': data.get('name', 'TBD').upper(),
				'Team_Code': data.get('teamCode', 'TBD').upper(),
				'Abbreviation': data.get('abbreviation', 'TBD'),
				'Team_Short_Name': data.get('shortName', 'TBD').upper(),
				'Location': data.get('locationName', 'TBD').upper(),
				'First_Year_Of_Play': data.get('firstYearOfPlay', 'TBD'),
				'Team_Link': f"{ BASE_URL }{ data.get('link', 'TBD') }",
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
					'League_Link': f"{ BASE_URL }{ data.get('league').get('link', 'TBD') }",
				})
			if 'venue' in data.keys():
				data_dump.update({
					'Venue_ID': data.get('venue').get('id', 'TBD'),
					'Venue_Name': data.get('venue').get('name', 'TBD'),
					'Venue_Link': f"{ BASE_URL }{ data.get('venue').get('link', 'TBD') }",
				})
			if 'division' in data.keys():
				data_dump.update({
					'Division_ID': data.get('division').get('id', 'TBD'),
					'Division_Name': data.get('division').get('name', 'TBD'),
					'Division_Link': f"{ BASE_URL }{ data.get('division').get('link', 'TBD') }",
				})
			if 'sport' in data.keys():
				data_dump.update({
					'Sport_ID': data.get('sport').get('id', 'TBD'),
					'Sport_Name': data.get('sport').get('name', 'TBD'),
					'Sport_Link': f"{ BASE_URL }{ data.get('sport').get('link', 'TBD') }",	
				})
			if 'springLeague' in data.keys():
				data_dump.update({
					'Spring_League_ID': data.get('springLeague').get('id', 'TBD'),
					'Spring_League_Name': data.get('springLeague').get('name', 'TBD'),
					'Spring_League_Link': f"{ BASE_URL }{ data.get('springLeague').get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


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


@st.cache
def List_MLB_Players(sport_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/sports/{sport_id}/players').json()
		for data in response['people']:
			data_dump = {
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
					'Current_Team_Link': f"{ BASE_URL }{ data.get('currentTeam').get('link', 'TBD') }",	
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
		response: dict = requests.get(f'{BASE_URL}/api/v1/league').json()
		for data in response['leagues']:
			data_dump = {
				'League_ID': data.get('id', 'TBD'),
				'League_Name': data.get('name', 'TBD'),
				'League_Link': f"{ BASE_URL }{ data.get('link', 'TBD') }",
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
		response: dict = requests.get(f'{BASE_URL}/api/v1/divisions').json()
		for data in response['divisions']:
			data_dump = {
				'Division_ID': data.get('id', 'TBD'),
				'Division_Name': data.get('name', 'TBD').upper(),
				'Division_Short_Name': data.get('nameShort', 'TBD').upper(),
				'Abbreviation': data.get('abbreviation', 'TBD'),
				'Division_Link': f"{ BASE_URL }{ data.get('link', 'TBD') }",
				'Has_Wild_Card': 'TBD' if 'hasWildcard' not in data.keys() else 'Yes' 
					if data.get('hasWildcard') == True else 'No',
				'Playoff_Teams': data.get('numPlayoffTeams', 'TBD')
			}
			if 'league' in data.keys():
				data_dump.update({
					'League_ID': data.get('league').get('id', 'TBD'),
					'League_Link': f"{ BASE_URL }{ data.get('league').get('link', 'TBD') }",
				})
			if 'sport' in data.keys():
				data_dump.update({
					'Sport_ID': data.get('sport').get('id', 'TBD'),
					'Sport_Link': f"{ BASE_URL }{ data.get('sport').get('link', 'TBD') }",
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
		request_url: str = f'{BASE_URL}/api/v1/schedule?sportId={sport_id}&startDate={start_date}&endDate={end_date}'
		response: dict = requests.get( request_url ).json()
		for day in response['dates']:
			for data in day['games']:
				data_dump = {
					'Game_Date': parser.parse( day['date'] ).strftime('%d-%m-%Y') 
						if 'date' in day.keys() else 'TBD',
					'Total_Games': day.get('totalGames', 'TBD'),
					'Game_ID': data.get('gamePk', 'TBD'),
					'Game_Link': f"{ BASE_URL }{ data.get('link', 'TBD') }",
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
						'Content_Link': f"{ BASE_URL }{ data.get('content').get('link', 'TBD') }",
					})
				if 'venue' in data.keys():
					data_dump.update({
						'Venue_ID': data.get('venue').get('id', 'TBD'),
						'Venue_Name': data.get('venue').get('name', 'TBD'),
						'Venue_Link': f"{ BASE_URL }{ data.get('venue').get('link', 'TBD') }",
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
								'Away_Team_Link': f"{ BASE_URL } { data['teams']['away']['team'].get('link', 'TBD') }",
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
								'Home_Team_Link': f"{ BASE_URL } { data['teams']['home']['team'].get('link', 'TBD') }",
							})
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Rosters(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/teams/{team_id}/roster').json()
		for data in response['roster']:
			data_dump = {
				'Team_id': team_id,
				'Jersey_Number': data.get('jerseyNumber', 'TBD'),
				'Position': data.get('position', 'TBD').get('name', 'TBD'),
				'Status': data.get('status', 'TBD').get('description', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Player_Name': data['person'].get('fullName', 'TBD'),
					'Player_Link': f"{ BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Personnel(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/teams/{team_id}/personnel').json()
		for data in response['roster']:
			data_dump = {
				'Team_ID': team_id,
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Player_Name': data['person'].get('fullName', 'TBD'),
					'Player_Link': f"{ BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Coaches(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/teams/{team_id}/coaches').json()
		for data in response['roster']:
			data_dump = {
				'Team_ID': team_id,
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Attendances(team_id: int) -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/attendance?teamId={team_id}').json()
		for data in response['records']:
			data_dump = {
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
					'Team_Link': f"{ BASE_URL }{ data['team'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Venues() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/venues').json()
		for data in response['venues']:
			dataset.append({
				'Venue_ID': data.get('id', 'TBD'),
				'Venue_Name': data.get('name', 'TBD'),
				'Venue_Link': f"{ BASE_URL }{ data.get('link', 'TBD') }",
			})
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Alumnis(team_id: int) -> dict:
	try:
		dataset, season = [], datetime.now().year
		response: dict = requests.get(f'{BASE_URL}/api/v1/teams/{team_id}/alumni?season={season}').json()
		for data in response['people']:
			data_dump = {
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
		response: dict = requests.get(f'{BASE_URL}/api/v1/standings?leagueId={league_id}').json()
		for record in response['records']:
			for data in record['teamRecords']:
				data_dump = {
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
						'Team_Link': f"{ BASE_URL }{ data['team'].get('link', 'TBD') }",
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
						'League_Link': f"{ BASE_URL }{ record['league'].get('link', 'TBD') }",
					})
				if 'sport' in record.keys():
					data_dump.update({
						'Sport_ID': record['sport'].get('id', 'TBD'),
						'Sport_Link': f"{ BASE_URL }{ record['sport'].get('link', 'TBD') }",
					})
				if 'division' in record.keys():
					data_dump.update({
						'Division_ID': record['division'].get('id', 'TBD'),
						'Division_Link': f"{ BASE_URL }{ record['division'].get('link', 'TBD') }",
					})
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Drafts() -> dict:
	try:
		dataset, year = [], datetime.now().year
		response: dict = requests.get(f'{BASE_URL}/api/v1/draft/{year}').json()
		for rounds in response['drafts']['rounds']:
			for data in rounds['picks']:
				data_dump = {
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
						'Team_Link': f"{ BASE_URL }{ data['team'].get('link', 'TBD') }",
						'ALL_Star_Status': data['team'].get('allStarStatus', 'TBD'),
					})
					if 'springLeague' in data['team'].keys():
						data_dump.update({
							'Spring_League_ID': data['team']['springLeague'].get('id', 'TBD'),
							'Spring_League_Name': data['team']['springLeague'].get('name', 'TBD'),
							'Spring_League_Link': f"{ BASE_URL } { data['team']['springLeague'].get('link', 'TBD') }",
						})
				print('\n', data_dump)
				dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_Umpires() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/jobs/umpires').json()
		for data in response['roster']:
			data_dump = {
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
				'Jersey_Number': data.get('jerseyNumber', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
		return { 'count' : len(dataset), 'data' : dataset }
	except Exception as ex:
		return { 'data' : { 'error' : ex } }


@st.cache
def List_MLB_DataCasters() -> dict:
	try:
		dataset: list = []
		response: dict = requests.get(f'{BASE_URL}/api/v1/jobs/datacasters').json()
		for data in response['roster']:
			data_dump = {
				'Job_ID': data.get('jobId', 'TBD'),
				'Job_Name': data.get('job', 'TBD'),
			}
			if 'person' in data.keys():
				data_dump.update({
					'Person_ID': data['person'].get('id', 'TBD'),
					'Person_Name': data['person'].get('fullName', 'TBD'),
					'Person_Link': f"{ BASE_URL }{ data['person'].get('link', 'TBD') }",
				})
			dataset.append( data_dump )
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

	if CATEGORY == 'About MLB':
		st.subheader('** About MLB **')
		st.write(""" The Major League Baseball (MLB) is an American Professional Baseball Organization and The 
			Oldest of the Major Professional Sports Leagues in the United States and Canada. A Total of 30 Teams 
			Play in Major League Baseball: 15 Teams in the National League (NL) and 15 in the American League (AL).
			The NL and AL were Formed as Separate Legal Entities in 1876 and 1901 Respectively. Beginning in 1903, 
			the Two Leagues Cooperated But Remained Legally Separate Entities. Both leagues Operated as Legally 
			Separate Entities Until They Merged into a Single Organization Led by the Commissioner of Baseball in 
			2000. MLB also Oversees Minor League Baseball, Which Comprises 256 Teams Affiliated With the Major 
			League Clubs. MLB and the World Baseball Softball Confederation Jointly Manage the International World 
			Baseball Classic tournament.""")
		st.markdown( f"<img src = 'https://www.mlbstatic.com/team-logos/league-on-dark/1.svg' width = 700 \
			height = 400>", unsafe_allow_html = True )

	elif CATEGORY == 'MLB Teams':
		try:
			st.subheader('** MLB Teams **')
			dataset = pandas.DataFrame( data = List_MLB_Teams()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Sports':
		try:
			st.subheader('** MLB Sports **')
			dataset = pandas.DataFrame( data = List_MLB_Sports()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Players':
		try:
			st.subheader('** MLB Players **')
			Sports: dict = { Sport['Sport_Name']: int(Sport['Sport_ID']) for Sport in List_MLB_Sports()['data'] }
			Sport: str = st.selectbox(label = 'Select MLB Sport', options = list(Sports.keys()) )
			st.write(f'** > Selected ** Sport Name = { Sport } | Sport ID = { Sports[Sport] } ')
			dataset = pandas.DataFrame( data = List_MLB_Players( sport_id = Sports[Sport] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Leagues':
		try:
			st.subheader('** MLB Leagues **')
			dataset = pandas.DataFrame( data = List_MLB_Leagues()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Divisions':
		try:
			st.subheader('** MLB Divisions **')
			dataset = pandas.DataFrame( data = List_MLB_Divisions()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Schedule':
		try:
			st.subheader('** MLB Schedule **')
			col_1, col_2, col_3 = st.beta_columns((3, 2, 2))
			Sports: dict = { Sport['Sport_Name']: int(Sport['Sport_ID']) for Sport in List_MLB_Sports()['data'] }
			Sport: str = col_1.selectbox(label = 'Select MLB Sport', options = list(Sports.keys()) )
			Start_Date = col_2.date_input(label = 'Start Date', value = (datetime.now() - timedelta(days = 5)) )
			End_Date = col_3.date_input(label = 'End Date', value = (datetime.now() + timedelta(days = 30)) )
			st.write(f'** > Selected ** MLB Sport Name =  { Sport } | Sport ID = { Sports[Sport] } ')
			st.write(f'** > Selected ** Start Date = { Start_Date } | End Date = { End_Date } ')
			dataset = pandas.DataFrame( data = List_MLB_Schedule( sport_id = Sports[Sport], start_date = Start_Date, 
				end_date = End_Date )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Team Rosters':
		try:
			st.subheader('** MLB Team Rosters **')
			Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
			Team: str = st.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
			st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
			dataset = pandas.DataFrame( data = List_MLB_Rosters( team_id = Teams[Team] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Team Personnel':
		try:
			st.subheader('** MLB Team Personnel **')
			Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
			Team: str = st.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
			st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
			dataset = pandas.DataFrame( data = List_MLB_Personnel( team_id = Teams[Team] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Team Coaches':
		try:
			st.subheader('** MLB Team Coaches **')
			Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
			Team: str = st.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
			st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
			dataset = pandas.DataFrame( data = List_MLB_Coaches( team_id = Teams[Team] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Attendances':
		try:
			st.subheader('** MLB Attendances **')
			Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
			Team: str = st.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
			st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
			dataset = pandas.DataFrame( data = List_MLB_Attendances( team_id = Teams[Team] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Venues':
		try:
			st.subheader('** MLB Venues **')
			dataset = pandas.DataFrame( data = List_MLB_Venues()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Alumnis':
		try:
			st.subheader('** MLB Alumnis **')
			Teams: dict = { Team['Team_Name']: int(Team['Team_ID']) for Team in List_MLB_Teams()['data'] }
			Team: str = st.selectbox(label = 'Select MLB Team', options = list(Teams.keys()) )
			st.write(f'** > Selected ** Team Name = { Team } | Team ID = { Teams[Team] } ')
			dataset = pandas.DataFrame( data = List_MLB_Alumnis( team_id = Teams[Team] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB League Standings':
		try:
			st.subheader('** MLB League Standings **')
			Leagues: dict = { League['League_Name']: int(League['League_ID']) for League in List_MLB_Leagues()['data'] }
			League: str = st.selectbox(label = 'Select MLB League', options = list(Leagues.keys()) )
			st.write(f'** > Selected ** MLB League Name =  { League } | League ID = { Leagues[League] } ')
			dataset = pandas.DataFrame( data = List_MLB_League_Standings( league_id = Leagues[League] )['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Drafts':
		try:
			st.subheader('** MLB Drafts **')
			dataset = pandas.DataFrame( data = List_MLB_Drafts()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB Umpires':
		try:
			st.subheader('** MLB Umpires **')
			dataset = pandas.DataFrame( data = List_MLB_Umpires()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'MLB DataCasters':
		try:
			st.subheader('** MLB DataCasters **')
			dataset = pandas.DataFrame( data = List_MLB_Umpires()['data'] )
			dataset.fillna('TBD', inplace = True)
			st.markdown( body = Excel_Downloader( df = dataset ), unsafe_allow_html = True)
			st.dataframe( data = dataset )
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')



#----------------------------------------------------------------------------------------------------------------------#

## Execute / Run the Main Code!

if __name__ == '__main__':
	EXECUTE_MAIN()

#----------------------------------------------------------------------------------------------------------------------#