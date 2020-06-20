import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g


def stringifyLyrics(songs_df: pd.DataFrame):
	lyrics = ""
	for ind in songs_df.index: 
		lyrics += songs_df['Lyrics'][ind]
	return lyrics 

def access_sheet(key):
	# Get access to spreadsheet
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('MarkovBot.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open_by_key(key).worksheet("Master")

	# Save Lyrics
	lyrics = ""
	for l in sheet.col_values(4):
		lyrics += l
	return lyrics

def upload_sheet(songs_df: pd.DataFrame, key):
	# Get access to spreadsheet
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('MarkovBot.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open_by_key(key).sheet1

	wks_name = 'Master'
	d2g.upload(songs_df, key, wks_name, credentials=creds, row_names=True)

def save_model(json, key):
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('MarkovBot.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open_by_key(key).worksheet("JSON")

	counter = 1
	while (len(json) > 50000):
		to_save = json[:50000]
		sheet.update("A" + str(counter), to_save)
		json = json[50000:]
		counter += 1
	if (len(json) > 0):
		sheet.update("A" + str(counter), json)
	sheet.update("B1", counter)

def get_model(key):
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('MarkovBot.json', scope)
	client = gspread.authorize(creds)
	sheet = client.open_by_key(key).worksheet("JSON")

	counter = 1
	json = ""

	num_cells = sheet.get("B1").first()
	for i in range(int(num_cells)):
		next_val = sheet.get("A" + str(counter)).first()
		json += next_val
		counter += 1
		
	return json