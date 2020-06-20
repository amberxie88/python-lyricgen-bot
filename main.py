from GeniusArtistDataCollect import GeniusArtistDataCollect
from utils import stringifyLyrics, access_sheet, upload_sheet, save_model, get_model
import pandas as pd
import warnings
import os
from os import environ
import markovify
from dotenv import load_dotenv, find_dotenv

ARTIST_NAME = 'Lorde'
ALBUMS = ['Melodrama']
SPREADSHEET_KEY = environ.get('SPREADSHEET_KEY')

warnings.filterwarnings('ignore')
load_dotenv(find_dotenv())

# Get the CSV file 
'''
if os.path.isfile('{}.csv'.format(ARTIST_NAME)):
	songs_df = pd.DataFrame.from_csv('{}.csv'.format(ARTIST_NAME))
else:
	# Get data
	client_access_token = environ.get('GENIUS_CLIENT_ID')
	g = GeniusArtistDataCollect(client_access_token, ARTIST_NAME, ALBUMS)
	songs_df = g.get_artist_songs()
	#lyrics_str = g.get_corresponding_lyrics()
	songs_df.to_csv('{}.csv'.format(ARTIST_NAME))
'''

# Get the lyrics
client_access_token = environ.get('GENIUS_CLIENT_ID')
g = GeniusArtistDataCollect(client_access_token, ARTIST_NAME, ALBUMS)
songs_df = g.get_artist_songs()

print(songs_df)

# Now push songs_df it to Google Sheets
upload_sheet(songs_df, SPREADSHEET_KEY)

# Using Pandas dataframe, create string
lyrics = access_sheet(SPREADSHEET_KEY)


# Markovify
text_model = markovify.NewlineText(lyrics)

# Save model in sheets
save_model(text_model.to_json(), SPREADSHEET_KEY)

model_json = get_model(SPREADSHEET_KEY)

# Retrieve model
reconstituted_model = markovify.Text.from_json(model_json)

for i in range(5):
    print(text_model.make_sentence())

for i in range(5):
	print(reconstituted_model.make_sentence())
    